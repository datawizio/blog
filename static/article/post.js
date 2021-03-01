function putLike() {
  const postId = $("#post-id").value();
  $.ajax({
    url: "",
    method: "POST",
    
    success: function() {
      loadComments();
      $("#form-comment")[0].reset();
    }
  })
}



function sendComment(comment) {
  const postId = $("#post-id").val();
  $.ajax({
    url: `/api/article/posts/${postId}/comments/`,
    method: "POST",
    data: comment,
    success: function() {
      loadComments();
      $("#form-comment")[0].reset();
    }
  })
}

function showComments(comments) {
  $(".comments-list").html("")
  comments.forEach((comment) => {
    const el = $("<div></div>").html(comment);
    $(".comments-list").append(comment)
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
    const array = $('#form').serializeArray();
    const data = {};
    array.forEach(function(item) {
      data[item["name"]] = item["value"];
    })

    sendComment(data);
    return false;
  })
})