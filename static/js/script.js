document.addEventListener("DOMContentLoaded", function () {
  // JavaScript code

  /* ///////////////////////////////////////

    THESE FOLLOWING SCRIPTS ONLY FOR BASIC USAGE, 
    For sliders, interactions, and other

    */ ///////////////////////////////////////

  //////////////////////// Prevent closing from click inside dropdown
  document.querySelectorAll(".dropdown-menu").forEach(function (dropdown) {
    dropdown.addEventListener("click", function (e) {
      e.stopPropagation();
    });
  });

  document.querySelectorAll(".js-check :radio").forEach(function (radio) {
    radio.addEventListener("change", function () {
      var check_attr_name = radio.getAttribute("name");
      if (radio.checked) {
        document
          .querySelectorAll('input[name="' + check_attr_name + '"]')
          .forEach(function (el) {
            el.closest(".js-check").classList.remove("active");
          });
        radio.closest(".js-check").classList.add("active");
        // item.find('.radio').find('span').textContent = 'Add';
      } else {
        radio.closest(".js-check").classList.remove("active");
        // item.find('.radio').find('span').textContent = 'Unselect';
      }
    });
  });

  document.querySelectorAll(".js-check :checkbox").forEach(function (checkbox) {
    checkbox.addEventListener("change", function () {
      var check_attr_name = checkbox.getAttribute("name");
      if (checkbox.checked) {
        checkbox.closest(".js-check").classList.add("active");
        // item.find('.radio').find('span').textContent = 'Add';
      } else {
        checkbox.closest(".js-check").classList.remove("active");
        // item.find('.radio').find('span').textContent = 'Unselect';
      }
    });
  });

  //////////////////////// Bootstrap tooltip
  var tooltips = document.querySelectorAll('[data-toggle="tooltip"]');
  if (tooltips.length > 0) {
    tooltips.forEach(function (tooltip) {
      new bootstrap.Tooltip(tooltip);
    });
  }
});
