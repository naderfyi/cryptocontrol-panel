$(document).ready(function () {
  $(".data-table").each(function (_, table) {
    $(table).DataTable({
        order: [[0, 'asc']],
    });
  });
});




