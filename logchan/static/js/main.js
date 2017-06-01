function displayError(err){
  alert(err);
}

function disableForm() {
  document.querySelectorAll('form input').forEach(elt => {
    elt.readonly = true;
  });
}

function enableForm() {
  grecaptcha.reset();
  document.querySelectorAll('form input').forEach(elt => {
    elt.readonly = false;
  });
  document.querySelector('form').reset();
}

