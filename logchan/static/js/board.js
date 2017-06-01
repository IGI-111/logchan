const CURRENT_BOARD = document.querySelector("#threadForm *[name=board]").value;

function sendThreadForm (e) {
  e.preventDefault();    // stop form from submitting

  disableForm();

  const threadData = new FormData();
  threadData.set('board', CURRENT_BOARD);
  threadData.set('subject', document.querySelector('#threadForm *[name=subject]').value);
  threadData.set('g-recaptcha-response', document.querySelector('#threadForm *[name=g-recaptcha-response]').value);
  threadData.set('csrfmiddlewaretoken', document.querySelector('#threadForm *[name=csrfmiddlewaretoken]').value);

  const postData = new FormData();
  postData.set('message', document.querySelector('#threadForm *[name=message]').value);
  postData.set('username', document.querySelector('#threadForm *[name=user_name]').value);
  postData.set('image', document.querySelector('#threadForm *[name=image]').files[0]);
  postData.set('g-recaptcha-response', document.querySelector('#threadForm *[name=g-recaptcha-response]').value);
  postData.set('csrfmiddlewaretoken', document.querySelector('#threadForm *[name=csrfmiddlewaretoken]').value);

  const threadRequest = new XMLHttpRequest();
  threadRequest.onreadystatechange = () => {
    if (threadRequest.readyState === XMLHttpRequest.DONE && threadRequest.status === 201) {
      const threadId = JSON.parse(threadRequest.response).id;
      postData.set('thread', threadId);

      // now post the OP
      const postRequest = new XMLHttpRequest();
      postRequest.onreadystatechange = () => {
        enableForm();
        if(postRequest.readyState === XMLHttpRequest.DONE && postRequest.status === 201) {
          reloadThreads();

          // redirect to thread
          window.location.href = `/board/${CURRENT_BOARD}/thread/${threadId}/`;
        }
      }
      postRequest.open('POST', '/api/post/', true);
      postRequest.send(postData);
    }
  };
  threadRequest.open('POST', '/api/thread/', true);
  threadRequest.send(threadData);
}

function disableForm() {
  document.querySelectorAll('#threadForm input').forEach(elt => {
    elt.readonly = true;
  });
}

function enableForm() {
  document.querySelectorAll('#threadForm input').forEach(elt => {
    elt.readonly = false;
  });
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
    a.setAttribute('href', `thread/${thread.id}`);
    const subject = document.createTextNode(thread.subject);
    a.appendChild(subject);
    node.appendChild(a);

    threadList.appendChild(node);
  });
}

document.addEventListener("DOMContentLoaded", function() {
  document.querySelector('#threadForm').addEventListener('submit', sendThreadForm);
});
