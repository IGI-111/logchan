const CURRENT_THREAD = parseInt(document.querySelector("#postForm input[name=thread]").value);

function disableForm () {
  document.querySelectorAll('#postForm input').forEach(elt => {
    elt.readonly = true;
  });
}

function enableForm () {
  document.querySelectorAll('#postForm input, textarea').forEach(elt => {
    elt.readonly = false;
  });
}

function sendPostForm (e) {
  e.preventDefault(); // stop form from submitting

  disableForm();

  const form = document.querySelector('#postForm');

  const data = new FormData();
  data.set('thread', CURRENT_THREAD);
  data.set('message', document.querySelector('#postForm textarea[name=message]').value);
  data.set('user_name', document.querySelector('#postForm input[name=user_name]').value);
  const image = document.querySelector('#postForm input[name=image]').files[0];
  if(image){
    data.set('image', image);
  }

  const request = new XMLHttpRequest();

  request.onreadystatechange = () => {
    enableForm();
    if(request.readyState === XMLHttpRequest.DONE && request.status === 201) {
      reloadPosts();
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

    if(post.image){
      const img = document.createElement('img');
      img.setAttribute('src', post.image);
      img.setAttribute('alt', post.id);
      node.appendChild(img);
    }

    const p = document.createElement('p');
    const message = document.createTextNode(post.message);
    p.appendChild(message);
    node.appendChild(p);

    postList.appendChild(node);
  });
  setupListeners();
}

function toggleImage (e) {
  e.preventDefault();
  e.target.classList.toggle('full');
}

function setupListeners() {
  document.querySelector('#postForm').addEventListener('submit', sendPostForm);
  document.querySelectorAll('#posts img').forEach(e => {
    e.addEventListener('click', toggleImage);
  });
}

document.addEventListener("DOMContentLoaded", setupListeners);

