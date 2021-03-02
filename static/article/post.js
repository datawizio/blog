function putLike(postId) {
  $.ajax({
    url: `/api/article/posts/${postId}/like/`,
    method: "POST",
    success: function(res) {
      console.log(res)
      $(`.btn-like[data-post=${postId}] span`).html(res.likes);
    }
  })
}

function sendComment(comment) {
  const postId = $("#post-id").val();
  $.ajax({
    url: `/api/article/posts/${postId}/comments/`,
    method: "POST",
    data: JSON.stringify(comment ),
    contentType: "application/json; charset=utf-8",
    success: function() {
      loadComments();
      $("#form-comment")[0].reset();
    }
  })
}

function showComments(comments) {
  $(".comments-list").html("")
  comments.forEach((comment) => {
    const el = $("<div class='pt-2'></div>").html(`
    <hr /><b>${comment.author}</b>: ${comment.body}
    `);
    $(".comments-list").append(el)
  })

}

function loadComments() {
  const postId = $("#post-id").val();
  $(".comments-list").html("Loading...")
  $.ajax({
    url: `/api/article/posts/${postId}/comments/`,
    method: "GET",
    success: function(data) {
      showComments(data.results);
    }
  })

}

$(document).ready(function() {
  loadComments();
  $("#form-comment").on("submit", function() {
    const array = $('#form-comment').serializeArray();
    const data = {};
    array.forEach(function(item) {
      data[item["name"]] = item["value"];
    })

    sendComment(data);
    return false;
  })

  $(".btn-like").on("click", function() {
    putLike($(this).data("post"));
  })
})