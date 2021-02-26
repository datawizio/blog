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
  $.ajax({
    url: "",
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
  $(".comments-list").html("Loading...")
  $.ajax({
    url: "",
    method: "GET",
    success: function() {
      showComments();
    }
  })

}

$(document).ready(function() {
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