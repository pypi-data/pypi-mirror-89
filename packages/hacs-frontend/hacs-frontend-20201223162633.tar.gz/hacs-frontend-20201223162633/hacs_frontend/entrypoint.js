
try {
  new Function("import('/hacsfiles/frontend/e.be336fea.js')")();
} catch (err) {
  var el = document.createElement('script');
  el.src = '/hacsfiles/frontend/e.be336fea.js';
  document.body.appendChild(el);
}
  