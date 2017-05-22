const CURRENT_BOARD = document.querySelector("#threadForm input[name=board]").value;

function sendThreadForm(e){
  e.preventDefault();    //stop form from submitting

  const threadData = new FormData();
  threadData.set('board', CURRENT_BOARD);
  threadData.set('subject', document.querySelector('#threadForm input[name=subject]').value);

  const postData = new FormData();
  postData.set('message', document.querySelector('#threadForm textarea[name=message]').value);
  postData.set('username', document.querySelector('#threadForm input[name=user_name]').value);
  postData.set('image', document.querySelector('#threadForm input[name=image]').value);

  const threadRequest = new XMLHttpRequest();
  threadRequest.onreadystatechange = () => {
    if(threadRequest.readyState === XMLHttpRequest.DONE && threadRequest.status === 201) {
      const threadId = JSON.parse(threadRequest.response).id;
      postData.set('thread', threadId);

      // now post the OP
      const postRequest = new XMLHttpRequest();
      postRequest.onreadystatechange = () => {
        if(postRequest.readyState === XMLHttpRequest.DONE && postRequest.status === 201) {
          reloadThreads();
        }
      }
      postRequest.open('POST', '/api/post/', true);
      postRequest.send(postData);
    }
  };
  threadRequest.open('POST', '/api/thread/', true);
  threadRequest.send(threadData);
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
