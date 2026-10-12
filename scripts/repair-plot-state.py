"""Guarded plotting-state repair. Does not replace statistical estimators."""
from pathlib import Path
import hashlib,re
p=Path('screenr.html');raw=p.read_bytes()
assert hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()=='d558b6bf4df90fc15a9f3552a54b1c5fd7cbfb0c'
t=raw.decode();marker="const STAT_LOGIC = document.getElementById('statLogicCode').textContent;"
assert t.count(marker)==1
bootstrap="""// Explicit session state needed by example import, filtering and dependent plots.
let records = [], decisions = new Map(), extractions = new Map();
let robAssessments = new Map(), qaAssessments = new Map(), provenancePointers = new Map();
let auditLogs = [], selectedRecord = null, currentFilter = 'all', currentScreener = 'screener1';
let recordListScroller = null, recordListVirtual = false, recordListCache = [];
let recordListItemHeight = 110, recordListLastRange = {start:-1,end:-1}, recordListResizeTimeout = null;
let extractionFieldOptions = null, extractionFieldLabelMap = null, extractionLabelToKeyMap = null;
let searchDebounce = null, computeWorker = null, workerCallbacks = new Map(), workerCallId = 0;
const VIRTUALIZATION_THRESHOLD = 500, VIRTUALIZATION_GAP = 8, VIRTUALIZATION_OVERSCAN = 5;
const EXTRACTION_ROLES = ['screener1','screener2','adjudicator','final'];
const STATUS_CLASSES = new Set(['include','exclude','maybe','conflict','duplicate']);
const PROV_LOW_THRESHOLD = 50, PROV_FULL_THRESHOLD = 100;
function updateStatusBar() {
  updateFilterCounts();
  updateHeaderProgress();
  const count = document.getElementById('recordCount');
  if (count) count.textContent = getFilteredRecords().length + ' / ' + records.length + ' records';
}

"""
for variable in ['currentFilter','selectedRecord','VIRTUALIZATION_THRESHOLD','EXTRACTION_ROLES']:
 assert not re.search(r'\b(?:let|const|var)\s+'+variable+r'\b',t), variable
t=t.replace(marker,bootstrap+marker,1)
a=t.index('function loadExampleDataset() {');b=t.index('// CONTEXTUAL TOOLTIPS',a)
loader=t[a:b]
needle='  // BCG Vaccine Meta-Analysis Dataset (classic example)';assert loader.count(needle)==1
loader=loader.replace(needle,"  if (records.length && !confirm('Replace this in-memory session with the BCG example? Existing saved project files are not changed.')) return;\n"+needle,1)
needle='  // Add to project';assert loader.count(needle)==1
loader=loader.replace(needle,"""  // Use the same stores as imported data; do not maintain stale demo-only fields.
  decisions = new Map(); extractions = new Map();
  robAssessments = new Map(); qaAssessments = new Map(); provenancePointers = new Map();
  selectedRecord = null; currentFilter = 'all';
  for (const d of bcgData) {
    const id=String(d.id);
    decisions.set(id,{screener1:'include',screener2:'include',final:'include',reason:'Built-in example'});
    extractions.set(id,{screener1:{},screener2:{},adjudicator:{},updatedAt:{},final:{
      effect_type:'rr',effect:String(Math.exp(d.yi)),
      ci_lo:String(Math.exp(d.yi-1.959964*Math.sqrt(d.vi))),
      ci_hi:String(Math.exp(d.yi+1.959964*Math.sqrt(d.vi))),
      treatment_n:String(d.treated_n),control_n:String(d.control_n),
      events_tx:String(d.treated_events),events_ctrl:String(d.control_events)
    }});
  }
  filterCache.query=null;filterCache.filter=null;filterCache.results=null;
  // Add to project""",1)
assert loader.count('    id: d.id,')==1;loader=loader.replace('    id: d.id,','    id: String(d.id),',1)
t=t[:a]+loader+t[b:]
a=t.index('function showSensitivityAnalysis() {');b=t.index('  if (includedStudies.length < 3)',a);old=t[a:b]
for needle,replacement in [
 ("    if (rec.finalDecision !== 'include') return;","    if (getDecisionForRecord(rec.id)?.status !== 'include') return;"),
 ('    const ext = rec.extracted || {};','    const ext = getPreferredExtractionData(rec.id) || {};'),
 ('parseFloat(ext.effect_size)','parseFloat(ext.effect)'),('parseFloat(ext.ci_lower)','parseFloat(ext.ci_lo)'),('parseFloat(ext.ci_upper)','parseFloat(ext.ci_hi)')]:
 assert old.count(needle)==1;old=old.replace(needle,replacement,1)
t=t[:a]+old+t[b:]
# The result engine returns effects/SEs but not these display-only diagnostic
# fields. Compute them with the existing routines instead of dereferencing undefined.
a=t.index('function showMetaAnalysis() {');b=t.index('  const forestPlot =',a)
old=t[a:b];needle='  const metaResult = calculateMetaAnalysis(includedStudies, state.metaSettings);'
assert old.count(needle)==1
old=old.replace(needle,needle+"\n  metaResult.eggerTest = calculateEggersTest(metaResult.transformedEffects, metaResult.ses);\n  metaResult.beggTest = calculateBeggsTest(metaResult.transformedEffects, metaResult.ses);",1)
t=t[:a]+old+t[b:]
style='\n<style id="screenr-responsive-analysis-plots">.modal-body svg { max-width:100%; height:auto; } .modal { max-width:95vw; }</style>\n'
assert t.count('</head>')==1;t=t.replace('</head>',style+'</head>',1)
p.write_bytes(t.encode())
print('Explicit session state and canonical plotting connections repaired; statistical estimator routines unchanged.')
