const CURRENT_BOARD = document.querySelector("#threadForm *[name=board]").value;

function sendThreadForm (e) {
  e.preventDefault();    // stop form from submitting

  disableForm();

  const data = new FormData();
  data.set('board', CURRENT_BOARD);
  data.set('subject', document.querySelector('#threadForm *[name=subject]').value);
  data.set('message', document.querySelector('#threadForm *[name=message]').value);
  data.set('username', document.querySelector('#threadForm *[name=user_name]').value);
  data.set('image', document.querySelector('#threadForm *[name=image]').files[0]);
  data.set('g-recaptcha-response', document.querySelector('#threadForm *[name=g-recaptcha-response]').value);
  data.set('csrfmiddlewaretoken', document.querySelector('#threadForm *[name=csrfmiddlewaretoken]').value);

  const request = new XMLHttpRequest();
  request.onreadystatechange = () => {
    if (request.readyState === XMLHttpRequest.DONE && request.status === 201) {
        enableForm();
          reloadThreads();

          // redirect to thread
          window.location.href = `/board/${CURRENT_BOARD}/thread/${threadId}/`;
    } else if(request.readyState === XMLHttpRequest.DONE) {
      displayError(request.response);
    }
  };
  request.open('POST', '/post_thread/', true);
  request.send(data);
}

function reloadThreads() {
  const request = new XMLHttpRequest();
  request.onreadystatechange = () =>  {
    if(request.readyState === XMLHttpRequest.DONE && request.status === 200) {
      const data = JSON.parse(request.response);
      updateThreadDisplay(data);
    }
  };
  request.open('GET', `/api/board/${CURRENT_BOARD}/thread`, true);
  request.send();
}

function updateThreadDisplay(threads){
  const threadList = document.querySelector('#threads');

  // empty posts
  const range = document.createRange();
  range.selectNodeContents(threadList);
  range.deleteContents();

  threads.forEach(thread => {
    const node = document.createElement('li');

    const a = document.createElement('a');
    a.setAttribute('href', `${thread.id}`);
    const subject = document.createTextNode(thread.subject);
    a.appendChild(subject);
    node.appendChild(a);

    threadList.appendChild(node);
  });
}

document.addEventListener("DOMContentLoaded", function() {
  document.querySelector('#threadForm').addEventListener('submit', sendThreadForm);
  const deleteForm = document.querySelector('#deleteBoardForm');
  if(deleteForm) {
    deleteForm.addEventListener('submit', deleteBoard);
  }
});

function deleteBoard(e) {
  e.preventDefault();    // stop form from submitting
  if(!confirm("Do you really want to delete this board ?")) {
    return;
  }
  const board = document.querySelector("#deleteBoardForm *[name=board]").value;
  const csrftoken = document.querySelector('#deleteBoardForm *[name=csrfmiddlewaretoken]').value;

  const deleteRequest = new XMLHttpRequest();
  deleteRequest.onreadystatechange = () => {
    if (deleteRequest.readyState === XMLHttpRequest.DONE && deleteRequest.status === 204) {
      window.location = "/";
    }
  };
  console.log("sending delete request");
  const url = '/api/board/' + board + '/';
  deleteRequest.open('DELETE', url, true);
  deleteRequest.setRequestHeader("X-CSRFToken", csrftoken);
  deleteRequest.send();
}

