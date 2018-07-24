import Cat from './cat'
document.addEventListener('DOMContentLoaded', function () {
  let tama = new Cat('tama');
  document.body.innerHTML = tama.greet();
});
