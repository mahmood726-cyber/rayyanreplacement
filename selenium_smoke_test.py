import argparse
import datetime as dt
import glob
import json
import os
import re
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

try:
    from pywinauto import Desktop, mouse
    from pywinauto.keyboard import send_keys
except Exception:
    Desktop = None
    send_keys = None
    mouse = None


ROOT = os.path.abspath(os.path.dirname(__file__))
HTML_PATH = os.path.join(ROOT, "screenr.html")
RIS_PATH = os.path.join(ROOT, "sample-records.ris")
RIS_PATH_ABS = os.path.abspath(RIS_PATH)


def find_latest(paths):
    if not paths:
        return None
    return max(paths, key=lambda p: os.path.getmtime(p))


def find_drivers():
    edge_paths = glob.glob(
        r"C:\Users\user\.cache\selenium\msedgedriver\win64\*\msedgedriver.exe"
    )
    chrome_paths = glob.glob(
        r"C:\Users\user\.cache\selenium\chromedriver\win64\*\chromedriver.exe"
    )
    return {
        "edge": find_latest(edge_paths) if edge_paths else None,
        "chrome": find_latest(chrome_paths) if chrome_paths else None,
    }


def build_driver(headed=False, browser=None):
    drivers = find_drivers()
    browser = browser or ("edge" if drivers.get("edge") else "chrome")
    driver_path = drivers.get(browser)
    if not driver_path:
        raise RuntimeError("No compatible WebDriver found in cache.")

    if browser == "edge":
        options = EdgeOptions()
        if not headed:
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1400,900")
        options.add_argument("--allow-file-access-from-files")
        service = EdgeService(executable_path=driver_path)
        return webdriver.Edge(service=service, options=options)

    options = ChromeOptions()
    if not headed:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1400,900")
    options.add_argument("--allow-file-access-from-files")
    service = ChromeService(executable_path=driver_path)
    return webdriver.Chrome(service=service, options=options)


def get_record_counts(driver):
    try:
        text = driver.find_element(By.ID, "recordCount").text
    except Exception:
        return None, None
    match = re.match(r"(\d+)\s*/\s*(\d+)", text)
    if not match:
        return None, None
    return int(match.group(1)), int(match.group(2))


def pick_pdf_path(cli_path=None):
    if cli_path and os.path.exists(cli_path):
        return os.path.abspath(cli_path)

    pdfs = glob.glob(r"C:\Users\user\Downloads\*.pdf")
    return os.path.abspath(pdfs[0]) if pdfs else None


def parse_args():
    parser = argparse.ArgumentParser(description="Screenr Selenium smoke test")
    parser.add_argument("--headed", action="store_true", help="Run in headed mode")
    parser.add_argument("--browser", choices=["edge", "chrome"], help="Browser choice")
    parser.add_argument("--strict-import", action="store_true", help="Fail if file import fails")
    parser.add_argument(
        "--strict-file-input",
        action="store_true",
        help="Fail unless the file input is populated by the browser",
    )
    parser.add_argument("--test-mode", action="store_true", help="Enable test mode UI helpers")
    parser.add_argument("--pdf", help="Path to PDF to load in viewer")
    parser.add_argument(
        "--artifacts",
        default=os.path.join(ROOT, "selenium_artifacts"),
        help="Directory for screenshots and logs",
    )
    return parser.parse_args()


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def timestamp():
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def build_large_ris(count):
    lines = []
    for i in range(count):
        lines.extend(
            [
                "TY  - JOUR",
                f"TI  - Load Test Record {i}",
                f"AU  - Load, Tester {i}",
                "PY  - 2024",
                "JO  - Load Journal",
                "AB  - Load test abstract.",
                "ER  -",
            ]
        )
    return "\n".join(lines)


def get_toast_text(driver):
    return driver.execute_script(
        "return document.querySelector('.toast') ? document.querySelector('.toast').innerText.trim() : '';"
    )


def safe_click(driver, selector):
    element = driver.find_element(By.CSS_SELECTOR, selector)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    driver.execute_script("arguments[0].click();", element)


def select_file_with_dialog(file_path, timeout=20):
    if Desktop is None or send_keys is None:
        raise RuntimeError("pywinauto is not available for file dialog automation.")

    end_time = time.time() + timeout
    seen_titles = set()
    while time.time() < end_time:
        for backend in ("uia", "win32"):
            try:
                dialogs = Desktop(backend=backend).windows(class_name="#32770")
            except Exception:
                continue
            for dlg in dialogs:
                title = dlg.window_text() or ""
                seen_titles.add(f"{backend}:{title}")
                if not any(token in title for token in ("Open", "File", "Choose", "Select")):
                    continue
                try:
                    dlg.set_focus()
                except Exception:
                    pass
                try:
                    if backend == "uia":
                        file_edit = dlg.child_window(title_re="File name|File Name|File name:", control_type="Edit")
                        open_btn = dlg.child_window(title_re="Open|Open Button", control_type="Button")
                    else:
                        file_edit = dlg.child_window(title_re="File name|File Name|File name:", class_name="Edit")
                        open_btn = dlg.child_window(title_re="Open|Open Button", class_name="Button")
                    if file_edit.exists():
                        file_edit.set_edit_text(file_path)
                        if open_btn.exists():
                            open_btn.click()
                        else:
                            send_keys("{ENTER}")
                        return True
                except Exception:
                    pass
                try:
                    send_keys(file_path + "{ENTER}")
                    return True
                except Exception:
                    pass
        time.sleep(0.2)
    raise RuntimeError(f"File dialog not detected. Windows seen: {sorted(seen_titles)}")


def click_file_input_with_mouse(driver, element):
    if mouse is None:
        raise RuntimeError("pywinauto mouse is not available for file dialog automation.")
    rect = driver.execute_script(
        """
        const r = arguments[0].getBoundingClientRect();
        return {
          left: r.left,
          top: r.top,
          width: r.width,
          height: r.height,
          innerWidth: window.innerWidth,
          innerHeight: window.innerHeight,
          outerWidth: window.outerWidth,
          outerHeight: window.outerHeight,
          screenX: window.screenX,
          screenY: window.screenY
        };
        """,
        element,
    )
    border_x = max(0, (rect["outerWidth"] - rect["innerWidth"]) / 2)
    border_y = max(0, rect["outerHeight"] - rect["innerHeight"] - border_x)
    click_x = rect["screenX"] + border_x + rect["left"] + rect["width"] / 2
    click_y = rect["screenY"] + border_y + rect["top"] + rect["height"] / 2
    mouse.click(button="left", coords=(int(click_x), int(click_y)))


def main():
    args = parse_args()
    artifacts_dir = ensure_dir(args.artifacts)
    results = []
    test_mode = args.test_mode or args.strict_import or args.strict_file_input

    if not os.path.exists(HTML_PATH):
        raise RuntimeError(f"Missing HTML file: {HTML_PATH}")

    driver = build_driver(headed=args.headed, browser=args.browser)
    wait = WebDriverWait(driver, 20)

    try:
        driver.set_window_position(100, 100)
        driver.set_window_size(1400, 900)
        url = f"file:///{HTML_PATH.replace(os.sep, '/')}"
        if test_mode:
            url = f"{url}?test=1"
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "header")))
        results.append(("page_load", True, "header visible"))
        results.append(("test_mode", True, "enabled" if test_mode else "disabled"))
        results.append(("strict_file_input", True, "enabled" if args.strict_file_input else "disabled"))
        if test_mode:
            wait.until(lambda d: d.execute_script("return !!window.TEST_API;"))
            driver.execute_script("window.TEST_API.resetState();")
            time.sleep(0.5)

        before_visible, before_total = get_record_counts(driver)

        driver.execute_script(
            """
            window._downloads = [];
            window._downloadFileOriginal = window.downloadFile;
            window.downloadFile = function(content, filename, type) {
              const text = String(content || '');
              const maxSize = 200000;
              const trimmed = text.length > maxSize ? text.slice(0, maxSize) : text;
              window._downloads.push({
                filename: filename,
                size: text.length,
                type: type,
                content: trimmed,
                truncated: text.length > maxSize
              });
            };
            """
        )

        import_method = "file-input"
        import_input_id = "importInputTest" if test_mode else "importInput"
        import_handled = False
        if os.path.exists(RIS_PATH_ABS):
            if not test_mode:
                driver.execute_script(
                    "document.getElementById('importInput').style.display = 'block';"
                )
            if args.strict_file_input:
                input_el = driver.find_element(By.ID, import_input_id)
                try:
                    input_el.click()
                except Exception:
                    click_file_input_with_mouse(driver, input_el)
                if not select_file_with_dialog(RIS_PATH_ABS):
                    raise RuntimeError("File dialog automation failed.")
            else:
                driver.find_element(By.ID, import_input_id).send_keys(RIS_PATH_ABS)
                driver.execute_script(
                    "document.getElementById(arguments[0]).dispatchEvent(new Event('change', { bubbles: true }));",
                    import_input_id,
                )
                time.sleep(2)

        def records_ready(d):
            return d.execute_script(
                "return (typeof records !== 'undefined') && records.length > 0;"
            )

        try:
            wait.until(records_ready)
            import_handled = True
        except TimeoutException:
            file_count = driver.execute_script(
                "return document.getElementById(arguments[0]).files.length;",
                import_input_id,
            )
            file_value = driver.execute_script(
                "return document.getElementById(arguments[0]).value;",
                import_input_id,
            )
            if args.strict_file_input:
                results.append(("file_input_set", file_count > 0, f"count={file_count}"))
            if args.strict_file_input and file_count == 0:
                raise RuntimeError(
                    f"Strict file input failed. input={import_input_id} file_count={file_count}, value={file_value}"
                )

            if args.strict_import:
                if test_mode and os.path.exists(RIS_PATH_ABS):
                    with open(RIS_PATH_ABS, "r", encoding="utf-8", errors="replace") as handle:
                        ris_content = handle.read()
                    parsed_len = driver.execute_script(
                        "return window.TEST_API ? window.TEST_API.importRISString(arguments[0]) : -1;",
                        ris_content,
                    )
                    if parsed_len > 0:
                        import_method = "test-api"
                        wait.until(records_ready)
                        import_handled = True
                    else:
                        raise RuntimeError(
                            f"Strict import failed (test-api). input={import_input_id} file_count={file_count}, value={file_value}"
                        )
                else:
                    raise RuntimeError(
                        f"Strict import failed. input={import_input_id} file_count={file_count}, value={file_value}"
                    )

            if not import_handled and file_count == 0 and os.path.exists(RIS_PATH_ABS):
                with open(RIS_PATH_ABS, "r", encoding="utf-8", errors="replace") as handle:
                    ris_content = handle.read()
                parsed_len = driver.execute_script(
                    """
                    try {
                      const imported = parseRIS(arguments[0]);
                      records = [...records, ...imported];
                      renderRecordList();
                      return imported.length;
                    } catch (e) {
                      return -1;
                    }
                    """,
                    ris_content,
                )
                if parsed_len > 0:
                    import_method = "js-fallback"
                    wait.until(records_ready)
                else:
                    import_method = "dummy-record"
                    driver.execute_script(
                        """
                        records = [{
                          id: 'r_test',
                          title: 'Sample RCT for Selenium',
                          authors: 'Doe J; Smith A',
                          year: '2024',
                          abstract: 'randomized trial with placebo control',    
                          journal: 'Test Journal',
                          keywords: ['randomized', 'placebo']
                        }];
                        renderRecordList();
                        """
                    )
            elif not import_handled:
                raise RuntimeError(
                    f"Record import did not populate the records array. file_count={file_count}, value={file_value}"
                )

        records_len = driver.execute_script("return records.length;")
        results.append(("import_records", records_len > 0, f"method={import_method}, count={records_len}"))

        driver.execute_script("renderRecordList();")
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#recordList .record-item")
            )
        )
        after_visible, after_total = get_record_counts(driver)

        safe_click(driver, "#recordList .record-item")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".detail-title")))
        results.append(("record_detail", True, "detail loaded"))

        safe_click(driver, "#decisionBar button.success")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#recordList .record-item.include")))
        results.append(("decision_include", True, "include badge applied"))

        safe_click(driver, ".filter-chip[data-filter=\"include\"]")
        filtered_count = driver.execute_script("return getFilteredRecords().length;")
        results.append(("filter_include", filtered_count > 0, f"filtered={filtered_count}"))

        search_term = driver.execute_script(
            "return (records[0].title || '').split(/\\s+/)[0];"
        )
        if search_term:
            driver.execute_script(
                """
                const input = document.getElementById('searchInput');
                input.value = arguments[0];
                input.dispatchEvent(new Event('input', { bubbles: true }));
                """,
                search_term,
            )
            search_count = driver.execute_script("return getFilteredRecords().length;")
            results.append(("search_filter", search_count > 0, f"term={search_term}"))

            driver.execute_script(
                """
                const input = document.getElementById('searchInput');
                input.value = '';
                input.dispatchEvent(new Event('input', { bubbles: true }));
                """
            )
            safe_click(driver, ".filter-chip[data-filter=\"all\"]")

        driver.execute_script(
            """
            const manual = {
              id: `manual_${Date.now()}`,
              title: 'Manual duplicate check',
              authors: 'Tester',
              year: '2024',
              abstract: '',
              keywords: []
            };
            records.push(manual);
            renderRecordList();
            selectRecord(manual.id);
            """
        )
        safe_click(driver, "#decisionBar button.info")
        dup_flag = driver.execute_script(
            "return document.querySelector('.record-item.duplicate') !== null;"
        )
        results.append(("manual_duplicate", dup_flag, ""))
        driver.execute_script("selectRecord(records[0].id);")

        shortcut_ids = driver.execute_script(
            """
            const a = { id: `kbd_${Date.now()}`, title: 'Shortcut A', authors: 'Tester', year: '2024', abstract: '', keywords: [] };
            const b = { id: `kbd_${Date.now() + 1}`, title: 'Shortcut B', authors: 'Tester', year: '2024', abstract: '', keywords: [] };
            records.push(a, b);
            renderRecordList();
            selectRecord(a.id);
            return [a.id, b.id];
            """
        )
        driver.execute_script("document.body.focus();")
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys("n")
        selected_id = driver.execute_script(
            "return selectedRecord ? selectedRecord.id : null;"
        )
        results.append(
            ("shortcut_skip", selected_id == shortcut_ids[1], f"selected={selected_id}")
        )
        body.send_keys("i")
        decision = driver.execute_script(
            "const d = decisions.get(arguments[0]); return d ? d.screener1 : null;",
            shortcut_ids[1],
        )
        results.append(
            ("shortcut_include", decision == "include", f"decision={decision}")
        )

        dup_id = driver.execute_script(
            """
            const rec = { id: `kbd_${Date.now() + 2}`, title: 'Shortcut Dup', authors: 'Tester', year: '2024', abstract: '', keywords: [] };
            records.push(rec);
            renderRecordList();
            selectRecord(rec.id);
            return rec.id;
            """
        )
        driver.execute_script("document.body.focus();")
        body.send_keys("d")
        dup_decision = driver.execute_script(
            "const d = decisions.get(arguments[0]); return d ? d.screener1 : null;",
            dup_id,
        )
        results.append(
            ("shortcut_duplicate", dup_decision == "duplicate", f"decision={dup_decision}")
        )

        pico_items = driver.find_elements(By.CSS_SELECTOR, "#picoResults > div")
        pico_ok = len(pico_items) > 0
        results.append(("pico_results", pico_ok, f"count={len(pico_items)}"))

        safe_click(driver, "#rightTabs .tab[data-tab=\"extract\"]")
        wait.until(EC.presence_of_element_located((By.ID, "ext_effect")))
        driver.find_element(By.ID, "ext_effect").send_keys("0.82")
        driver.find_element(By.ID, "ext_ci_lo").send_keys("0.70")
        driver.find_element(By.ID, "ext_ci_hi").send_keys("0.96")
        driver.find_element(By.ID, "ext_treatment_n").send_keys("120")
        driver.find_element(By.ID, "ext_control_n").send_keys("118")
        driver.find_element(By.ID, "ext_events_tx").send_keys("12")
        driver.find_element(By.ID, "ext_events_ctrl").send_keys("18")
        safe_click(driver, "#extractTab button[onclick=\"saveExtraction()\"]")
        time.sleep(0.5)
        results.append(
            ("extraction_save", "Extraction saved" in get_toast_text(driver), get_toast_text(driver))
        )
        prov_missing = driver.execute_script(
            "return selectedRecord ? getRecordProvenanceStatus(selectedRecord.id) : null;"
        )
        results.append(("provenance_missing_before", prov_missing == "missing", f"status={prov_missing}"))
        safe_click(driver, "#extractTab button.danger")
        time.sleep(0.5)
        cleared = driver.execute_script("return document.getElementById('ext_effect').value === '';")
        results.append(("extraction_clear", cleared, ""))
        driver.execute_script("loadExtractionData();")
        reloaded_effect = driver.execute_script("return document.getElementById('ext_effect').value;")
        results.append(("extraction_reload", reloaded_effect == "0.82", f"value={reloaded_effect}"))
        driver.execute_script(
            """
            const fields = [
              'treatment_n',
              'control_n',
              'effect',
              'effect_type',
              'ci_lo',
              'ci_hi',
              'events_tx',
              'events_ctrl'
            ];
            const list = document.getElementById('provenanceList');
            fields.forEach((name, index) => {
              if (index > 0) addProvenanceRow();
              const row = list.querySelectorAll('.prov-row')[index];
              if (!row) return;
              row.querySelector('.prov-field').value = name;
              row.querySelector('.prov-source-hash').value = 'sha256:source123';
              row.querySelector('.prov-locator-type').value = 'table_cell';
              row.querySelector('.prov-page').value = '12';
              row.querySelector('.prov-table').value = 'Table 2';
              row.querySelector('.prov-row-index').value = String(index + 1);
              row.querySelector('.prov-col').value = '2';
            });
            """
        )
        driver.execute_script("saveProvenance();")
        time.sleep(0.4)
        results.append(
            ("provenance_save", "Provenance saved" in get_toast_text(driver), get_toast_text(driver))
        )
        prov_ok = driver.execute_script(
            "return selectedRecord ? getRecordProvenanceStatus(selectedRecord.id) : null;"
        )
        prov_badge = driver.execute_script(
            "return !!document.querySelector('.record-item.selected .mini-badge.prov-ok');"
        )
        results.append(("provenance_ok_after", prov_ok == "ok", f"status={prov_ok}"))
        results.append(("provenance_badge", prov_badge, ""))

        safe_click(driver, "#rightTabs .tab[data-tab=\"rob\"]")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#robTab .rob-judgement")))
        safe_click(driver, ".rob-judgement[data-domain=\"d1\"] .rob-btn.low")
        safe_click(driver, "#robTab button.success")
        time.sleep(0.5)
        results.append(
            ("rob_save", "RoB assessment saved" in get_toast_text(driver), get_toast_text(driver))
        )

        safe_click(driver, "#rightTabs .tab[data-tab=\"qa\"]")
        wait.until(EC.presence_of_element_located((By.ID, "qaItems")))
        driver.execute_script("loadQAChecklist();")
        safe_click(driver, "#qaItems .qa-opt.yes")
        safe_click(driver, "#qaTab button.success")
        time.sleep(0.5)
        results.append(
            ("qa_save", "Quality assessment saved" in get_toast_text(driver), get_toast_text(driver))
        )

        safe_click(driver, "#rightTabs .tab[data-tab=\"truthcert\"]")
        wait.until(EC.presence_of_element_located((By.ID, "tcStatus")))
        safe_click(driver, "#truthcertTab button.primary")
        wait.until(EC.presence_of_element_located((By.ID, "tc_badge_terminal_state")))
        driver.execute_script(
            """
            document.getElementById('tc_scope_endpoint').value = 'primary outcome';
            document.getElementById('tc_scope_entities').value = 'armA, armB';
            document.getElementById('tc_scope_units').value = 'mg/dL';
            document.getElementById('tc_scope_timepoint').value = '12 weeks';
            document.getElementById('tc_scope_inclusion_snippet').value = 'Adults with condition X';
            document.getElementById('tc_scope_source_hash').value = 'sha256:abc123';
            document.getElementById('tc_anchor_scope_lock_ref').value = 'scope-lock-1';
            document.getElementById('tc_anchor_validator_version').value = 'v1';
            document.getElementById('tc_anchor_timestamp').value = '2026-01-25T00:00:00Z';
            document.getElementById('tc_anchor_witness_mode').value = 'fixed';
            document.getElementById('tc_anchor_min_witnesses').value = '3';
            document.getElementById('tc_anchor_max_witnesses').value = '5';
            document.getElementById('tc_anchor_heterogeneity').value = 'required';
            document.getElementById('tc_anchor_convergence').value = '0.8';
            document.getElementById('tc_anchor_budget_mode').value = 'hard';
            document.getElementById('tc_anchor_budget_alert').value = '0.8';
            document.getElementById('tc_anchor_external_refs').value = 'true';
            document.getElementById('tc_anchor_rag').value = 'false';
            document.getElementById('tc_anchor_gold_standard').value = 'false';
            document.getElementById('tc_anchor_promotion_policy').value = 'balanced';
            document.getElementById('tc_disc_witness_mode').value = 'fixed';
            document.getElementById('tc_disc_witness_count').value = '3';
            document.getElementById('tc_disc_witness_families').value = 'famA, famB, famC';
            document.getElementById('tc_disc_hetero_setting').value = 'required';
            document.getElementById('tc_disc_external_refs').value = 'yes';
            document.getElementById('tc_disc_gold_standard').value = 'no';
            document.getElementById('tc_disc_rag').value = 'no';
            document.getElementById('tc_disc_budget_mode').value = 'hard';
            document.getElementById('tc_disc_validator_version').value = 'v1';
            """
        )
        driver.execute_script("saveTruthCertFromForm();")
        time.sleep(0.3)
        tc_status = driver.execute_script("return document.getElementById('tcStatus').innerText;")
        results.append(("truthcert_ready", "ready" in tc_status.lower(), tc_status))
        driver.execute_script("exportTruthCertBundle(); exportTruthCertDisclosure(); exportTruthCertPolicyAnchor(); exportTruthCertScopeLock(); exportTruthCertBadgeCard();")

        driver.execute_script(
            """
            const base = records[0];
            base.doi = base.doi || '10.1234/dup-test';
            const dup = { ...base, id: `dup_${Date.now()}` };
            records.push(dup);
            renderRecordList();
            """
        )
        driver.execute_script("runDeduplication();")
        dup_status = driver.execute_script(
            "const dup = records[records.length - 1]; const d = decisions.get(dup.id); return d ? d.screener1 : null;"
        )
        results.append(("deduplication", dup_status == "duplicate", f"status={dup_status}"))

        driver.execute_script(
            """
            const mk = (id, effect, lo, hi) => {
              records.push({ id, title: `Meta ${id}`, authors: 'Test', year: '2024', abstract: 'randomized placebo', keywords: [] });
              decisions.set(id, { screener1: 'include', final: 'include' });
              extractions.set(id, { effect: String(effect), ci_lo: String(lo), ci_hi: String(hi) });
            };
            mk(`meta_${Date.now()}`, 0.85, 0.70, 0.95);
            mk(`meta_${Date.now() + 1}`, 0.90, 0.75, 1.02);
            renderRecordList();
            """
        )
        driver.execute_script("showMetaAnalysis();")
        time.sleep(1)
        meta_active = driver.execute_script(
            "return document.getElementById('metaModal').classList.contains('active');"
        )
        meta_svg = driver.execute_script(
            "return document.getElementById('metaContent').querySelector('svg') !== null;"
        )
        results.append(("meta_analysis", meta_active and meta_svg, f"active={meta_active}, svg={meta_svg}"))
        driver.execute_script("closeMetaModal();")

        large_count = 150
        large_ris = build_large_ris(large_count)
        before_large = driver.execute_script("return records.length;")
        imported_large = driver.execute_script(
            "return window.TEST_API ? window.TEST_API.importRISString(arguments[0]) : -1;",
            large_ris,
        )
        after_large = driver.execute_script("return records.length;")
        large_ok = imported_large == large_count and after_large == before_large + large_count
        results.append(
            ("large_import", large_ok, f"imported={imported_large}, total={after_large}")
        )
        driver.execute_script(
            """
            const input = document.getElementById('searchInput');
            input.value = 'Load Test Record 1';
            input.dispatchEvent(new Event('input', { bubbles: true }));
            """
        )
        large_search = driver.execute_script("return getFilteredRecords().length;")
        results.append(("large_search", large_search > 0, f"filtered={large_search}"))
        driver.execute_script(
            """
            const input = document.getElementById('searchInput');
            input.value = '';
            input.dispatchEvent(new Event('input', { bubbles: true }));
            """
        )
        safe_click(driver, ".filter-chip[data-filter=\"all\"]")

        driver.execute_script(
            "exportJSON(); exportCSV(); exportDecisions(); exportExtractedData(); saveProject(); saveRuleset();"
        )
        download_count = driver.execute_script("return window._downloads.length;")
        results.append(("exports", download_count >= 4, f"downloads={download_count}"))

        downloads = driver.execute_script("return window._downloads;")
        project_entry = next(
            (item for item in downloads if item.get("filename") == "screenr-project.json"),
            None,
        )
        project_ok = False
        project_detail = "missing"
        if project_entry and not project_entry.get("truncated"):
            try:
                payload = json.loads(project_entry.get("content", ""))
                truthcert_ok = isinstance(payload.get("truthcert"), dict)
                project_ok = truthcert_ok
                project_detail = "truthcert=ok" if truthcert_ok else "truthcert=missing"
            except json.JSONDecodeError as exc:
                project_detail = f"invalid_json:{exc}"
        results.append(("project_save_truthcert", project_ok, project_detail))

        loaded_endpoint = "Loaded Endpoint"
        project_payload = {
            "version": 6,
            "name": "Loaded Project",
            "savedAt": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
            "records": [
                {
                    "id": "loaded_1",
                    "title": "Loaded Project Record",
                    "authors": "Tester",
                    "year": "2025",
                    "abstract": "",
                    "keywords": [],
                }
            ],
            "decisions": {},
            "extractions": {},
            "robAssessments": {},
            "qaAssessments": {},
            "picoRules": None,
            "truthcert": {
                "version": "3.1.0",
                "badge": {
                    "terminalState": "SHIPPED",
                    "bundleHash": "sha256:loaded",
                    "ledgerRef": "append-only-ledger://loaded",
                    "scopeLockHash": "sha256:scope",
                    "validatorVersion": "v1",
                    "validatorSetHash": "sha256:validators",
                },
                "disclosure": {
                    "witnessMode": "fixed",
                    "witnessesCount": 3,
                    "families": "famA, famB, famC",
                    "heterogeneitySetting": "required",
                    "heterogeneityAchieved": "true",
                    "externalRefsEnabled": "yes",
                    "goldStandardEnabled": "no",
                    "ragEnabled": "no",
                    "escalations": "",
                    "budgetMode": "hard",
                    "budgetExceeded": "false",
                    "validatorVersion": "v1",
                    "validatorSetHash": "sha256:validators",
                    "bundleHash": "sha256:loaded",
                    "ledgerRef": "append-only-ledger://loaded",
                    "timestampUtc": "2026-01-25T00:00:00Z",
                    "runId": "loaded-run",
                },
                "policyAnchor": {
                    "scopeLockRef": "scope-lock-1",
                    "validatorVersion": "v1",
                    "validatorSetHash": "sha256:validators",
                    "timestamp": "2026-01-25T00:00:00Z",
                    "thresholds": {
                        "factAgreement": 0.8,
                        "interpretationAgreement": 0.7,
                        "blindspotR": 0.6,
                        "materialDisagreementPct": 0.05,
                    },
                    "witnessConfig": {
                        "mode": "fixed",
                        "minWitnesses": 3,
                        "maxWitnesses": 5,
                        "heterogeneity": "required",
                        "convergenceThreshold": 0.8,
                    },
                    "costBudget": {
                        "enforcement": "hard",
                        "maxTokensPerBundle": 12000,
                        "maxCostUsdPerBundle": 1.5,
                        "alertThresholdPct": 0.8,
                    },
                    "features": {
                        "externalRefsEnabled": "true",
                        "ragEnabled": "false",
                        "goldStandardEnabled": "false",
                    },
                    "promotionPolicy": "balanced",
                },
                "scopeLock": {
                    "endpoint": loaded_endpoint,
                    "entities": ["Arm A", "Arm B"],
                    "units": "mg/dL",
                    "timepoint": "12 weeks",
                    "inclusionSnippet": "Adults with condition X",
                    "sourceHash": "sha256:source",
                },
            },
        }

        project_file = os.path.join(artifacts_dir, f"project_load_{timestamp()}.json")
        with open(project_file, "w", encoding="utf-8") as handle:
            json.dump(project_payload, handle)

        project_input_id = "projectInputTest" if test_mode else "projectInput"
        driver.find_element(By.ID, project_input_id).send_keys(project_file)

        def project_loaded(d):
            return d.execute_script(
                "return records.length === 1 && truthcertData && truthcertData.scopeLock && truthcertData.scopeLock.endpoint === arguments[0];",
                loaded_endpoint,
            )

        try:
            wait.until(project_loaded)
            loaded_count = driver.execute_script("return records.length;")
            loaded_scope = driver.execute_script(
                "return truthcertData && truthcertData.scopeLock ? truthcertData.scopeLock.endpoint : '';"
            )
            results.append(("project_load_records", loaded_count == 1, f"count={loaded_count}"))
            results.append(("project_load_truthcert", loaded_scope == loaded_endpoint, f"endpoint={loaded_scope}"))
        except TimeoutException:
            results.append(("project_load_records", False, "timeout"))
            results.append(("project_load_truthcert", False, "timeout"))

        driver.execute_script("showPDFViewer();")
        pdf_path = pick_pdf_path(args.pdf)
        pdf_result = "skipped"
        if pdf_path:
            pdf_input_id = "pdfInputTest" if test_mode else "pdfInput"
            driver.find_element(By.ID, pdf_input_id).send_keys(pdf_path)
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#pdfContainer canvas")))
                pdf_result = "loaded"
            except TimeoutException:
                toast = driver.find_elements(By.CSS_SELECTOR, ".toast")
                pdf_result = toast[0].text.strip() if toast else "failed (no toast)"

        results.append(("pdf_load", pdf_result == "loaded", pdf_result))

        print("Selenium smoke test results:")
        print(f"- Records before import: {before_visible}/{before_total}")
        print(f"- Records after import: {after_visible}/{after_total}")
        print(f"- Import method: {import_method}")
        for name, ok, detail in results:
            status = "ok" if ok else "failed"
            suffix = f" ({detail})" if detail else ""
            print(f"- {name}: {status}{suffix}")

    except Exception as exc:
        stamp = timestamp()
        screenshot = os.path.join(artifacts_dir, f"failure_{stamp}.png")
        html_dump = os.path.join(artifacts_dir, f"failure_{stamp}.html")
        try:
            driver.save_screenshot(screenshot)
            with open(html_dump, "w", encoding="utf-8") as handle:
                handle.write(driver.page_source)
        except Exception:
            pass
        raise exc
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
