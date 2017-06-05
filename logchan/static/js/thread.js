const CURRENT_THREAD = parseInt(document.querySelector("#postForm input[name=thread]").value);

const IS_LOGGED_IN = document.querySelector("#deleteThreadForm") != null;

function sendPostForm (e) {
  e.preventDefault(); // stop form from submitting

  disableForm();

  const form = document.querySelector('#postForm');
  const data = new FormData();
  data.set('thread', CURRENT_THREAD);
  data.set('message', document.querySelector('#postForm *[name=message]').value);
  data.set('user_name', document.querySelector('#postForm *[name=user_name]').value);
  const captcha = document.querySelector('#postForm *[name=g-recaptcha-response]');
  if(captcha) {
    data.set('g-recaptcha-response', captcha.value);
  }
  data.set('csrfmiddlewaretoken', document.querySelector('#postForm *[name=csrfmiddlewaretoken]').value);
  const image = document.querySelector('#postForm input[name=image]').files[0];
  if(image){
    data.set('image', image);
  }

  const request = new XMLHttpRequest();

  request.onreadystatechange = () => {
    enableForm();
    if(request.readyState === XMLHttpRequest.DONE && request.status === 201) {
      reloadPosts();
    } else if(request.readyState === XMLHttpRequest.DONE) {
      displayError(request.response);
    }
  };
  request.open('POST', '/api/post/', true);
  request.send(data);
}

function reloadPosts() {
  const request = new XMLHttpRequest();
  request.onreadystatechange = () => {
    if(request.readyState === XMLHttpRequest.DONE && request.status === 200) {
      const data = JSON.parse(request.response);
      updatePostDisplay(data);
    }
  };
  request.open('GET', `/api/thread/${CURRENT_THREAD}/post`, true);
  request.send();
}

function updatePostDisplay(posts){
  const postList = document.querySelector('#posts');

  // empty posts
  const range = document.createRange();
  range.selectNodeContents(postList);
  range.deleteContents();

  posts.forEach(post => {
    const node = document.createElement('li');


    const post_id = document.createElement('a');
    const post_id_text = document.createTextNode(post.id);
    post_id.appendChild(post_id_text);
    post_id.classList.add('post_id');
    node.appendChild(post_id);

    const user_name = document.createElement('span');
    user_name.classList.add('user_name');
    const user_name_text = document.createTextNode(post.user_name && post.user_name !== "" ?
      post.user_name :
      "Anonymous");
    user_name.appendChild(user_name_text);
    node.appendChild(user_name);

    if(IS_LOGGED_IN){
      const delete_button = document.createElement('button');
      delete_button.classList.add("deleteButton");
      delete_button.classList.add("deletePost");
      const delete_button_text = document.createTextNode("Delete post");
      delete_button.appendChild(delete_button_text);
      node.appendChild(delete_button);
      delete_button.addEventListener("click", removePost);
    }

    if(post.image){
      const img = document.createElement('img');
      img.setAttribute('src', post.image);
      img.setAttribute('alt', post.id);
      node.appendChild(img);
    }

    const p = document.createElement('p');
    const messageText = post.message.replace( /\n/g, "<br />" );
    p.innerHTML = messageText;
    node.appendChild(p);

    postList.appendChild(node);
  });
  setupListeners();
}

function toggleImage (e) {
  e.preventDefault();
  e.target.classList.toggle('full');
}

function respondToPost(e) {
  e.preventDefault();
  const postNumber = e.target.text;
  const textarea = document.querySelector('#postForm textarea');
  textarea.value += `>>${postNumber}\n`
  textarea.focus();
}

function deleteThread(e) {
  e.preventDefault();    // stop form from submitting
  if(!confirm("Do you really want to delete this thread ?")) {
    return;
  }
  const board = document.querySelector("#deleteThreadForm *[name=board]").value;
  const thread = document.querySelector("#deleteThreadForm *[name=thread]").value;
  const csrftoken = document.querySelector('#deleteThreadForm *[name=csrfmiddlewaretoken]').value;

  const deleteRequest = new XMLHttpRequest();
  deleteRequest.onreadystatechange = () => {
    if (deleteRequest.readyState === XMLHttpRequest.DONE && deleteRequest.status === 204) {
      window.location = "/" + board + "/";
    }
  };
  const url = '/api/thread/' + thread + '/';
  deleteRequest.open('DELETE', url, true);
  deleteRequest.setRequestHeader("X-CSRFToken", csrftoken);
  deleteRequest.send();
}

function removePost(e) {
  e.preventDefault();
  const thread = CURRENT_THREAD;
  console.log(e);
  const post = e.target.parentElement.querySelector(".post_id").text;
  const csrftoken = document.querySelector('#postForm *[name=csrfmiddlewaretoken]').value;

  const deleteRequest = new XMLHttpRequest();
  deleteRequest.onreadystatechange = () => {
    if (deleteRequest.readyState === XMLHttpRequest.DONE && deleteRequest.status === 204) {
      reloadPosts();
    }
  };
  const url = '/api/post/' + post + '/';
  deleteRequest.open('DELETE', url, true);
  deleteRequest.setRequestHeader("X-CSRFToken", csrftoken);
  deleteRequest.send();
}

function setupListeners() {
  document.querySelector('#postForm').addEventListener('submit', sendPostForm);
  document.querySelectorAll('#posts img').forEach(e => {
    e.addEventListener('click', toggleImage);
  });
  document.querySelectorAll('.post_id').forEach(e => {
    e.addEventListener('click', respondToPost);
  })
  if (IS_LOGGED_IN) {
    document.querySelector('#deleteThreadForm').addEventListener('submit', deleteThread);
    document.querySelectorAll('.deletePost').forEach(e => {
      e.addEventListener('click', removePost);
    })
  }
}

document.addEventListener("DOMContentLoaded", setupListeners);

