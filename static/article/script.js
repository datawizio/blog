import { serializeArray, getCookie } from "./utils.js";

async function putLike(postId) {
  try {
    const res = await fetch(`/api/article/posts/${postId}/like/`, {
      method: "POST",
      mode: "same-origin",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });
    const data = await res.json();
    const likesCount = document.querySelector(
      `.btn-like[data-post='${postId}'] span`
    );
    likesCount.textContent = data.likes;
  } catch (e) {
    console.error(e);
  }
}

function getPostId() {
  return document.getElementById("post-id")?.value;
}

async function sendComment(comment) {
  const postId = getPostId();
  if (!postId) return;

  try {
    await fetch(`/api/article/posts/${postId}/comments/`, {
      method: "POST",
      body: JSON.stringify(comment),
      mode: "same-origin",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });
    await loadComments();
  } catch (e) {
    console.error(e);
  }
}

function createComment(comment) {
  const block = document.createElement("div");
  const author = document.createElement("b");
  author.textContent = comment.author;
  const body = document.createElement("p");
  body.textContent = comment.body;
  block.appendChild(author);
  block.appendChild(body);
  return block;
}

function showComments(comments) {
  const list = document.querySelector(".comments-list");
  if (!list) return;
  list.innerHTML = "";
  comments.reverse().forEach((comment) => {
    const el = createComment(comment);
    list.appendChild(el);
  });
}

async function loadComments() {
  const postId = getPostId();
  if (!postId) return;
  try {
    const res = await fetch(`/api/article/posts/${postId}/comments/`);
    const data = await res.json();
    showComments(data.results);
  } catch (e) {
    console.error(e);
  }
}

window.addEventListener("DOMContentLoaded", function () {
  loadComments();
  document
    .getElementById("form-comment")
    ?.addEventListener("submit", async function (e) {
      e.preventDefault();
      const formData = serializeArray(this);

      const data = formData.reduce((obj, curr) => {
        obj[curr["name"]] = curr["value"];
        return obj;
      }, {});

      await sendComment(data);

      const collapse = new bootstrap.Collapse(
        document.getElementById("addComments")
      );
      collapse.hide();

      this.reset();
      return false;
    });

  document.querySelectorAll(".btn-like")?.forEach((btn) => {
    btn.addEventListener("click", function () {
      putLike(this.dataset.post);
    });
  });
});
