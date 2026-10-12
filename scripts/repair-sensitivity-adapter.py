from pathlib import Path
p=Path('screenr.html');t=p.read_text()
a=t.index('function showSensitivityAnalysis() {');b=t.index('  // Perform Influence Analysis',a)
old=t[a:b]
start=old.index('  // Perform Leave-One-Out Analysis')
old=old[:start]+"""  // The shared helpers return bare arrays, while this panel expects labelled
  // full/omitted/cumulative objects. Refit with the current main-analysis settings.
  const fit = rows => calculateMetaAnalysis(rows, {...state.metaSettings,
    useHKSJ: rows.length > 1 && state.metaSettings.useHKSJ});
  const fullMeta = fit(includedStudies);
  const leaveOneOutResults = {fullMeta, results: includedStudies.map((study,i) => {
    const omitted = fit(includedStudies.filter((_,j) => j!==i));
    return {...omitted, excluded:study,
      changePct: fullMeta.pooledEffect !== 0 ? 100*(omitted.pooledEffect-fullMeta.pooledEffect)/Math.abs(fullMeta.pooledEffect) : NaN};
  })};
  const cumulative = sorted => sorted.map((study,i) => ({...fit(sorted.slice(0,i+1)),
    study,nStudies:i+1}));
  const cumulativeResults = {
    byYear:cumulative([...includedStudies].sort((a,b) => (Number(a.year)||0)-(Number(b.year)||0))),
    byEffect:cumulative([...includedStudies].sort((a,b) => a.effect-b.effect))
  };

"""
t=t[:a]+old+t[b:]
# Scale SVG viewports, not just CSS boxes: retain the coordinate system on mobile.
needle='  const modal = document.getElementById(\'metaModal\');'
assert t.count(needle)==1
t=t.replace(needle,"""  document.querySelectorAll('#metaContent svg').forEach(svg => {
    if(!svg.hasAttribute('viewBox')) svg.setAttribute('viewBox',`0 0 ${svg.getAttribute('width')} ${svg.getAttribute('height')}`);
  });
"""+needle,1)
a=t.index('function showFunnelPlot() {');b=t.index('function closeFunnelModal()',a);old=t[a:b]
needle="  const svg = document.getElementById('funnelSvg');"
if needle in old:old=old.replace(needle,needle+"\n  svg.setAttribute('viewBox','0 0 600 400');",1)
t=t[:a]+old+t[b:]
needle='  window.sensitivityData = { studies, leaveOneOut, cumulative, influence, subgroup, robSensitivity };'
assert t.count(needle)==1
t=t.replace(needle,"""  document.querySelectorAll('#sensitivityModal svg').forEach(svg => {
    if(!svg.hasAttribute('viewBox')) svg.setAttribute('viewBox',`0 0 ${svg.getAttribute('width')} ${svg.getAttribute('height')}`);
  });
"""+needle,1)
p.write_text(t)
