var maxHeight = 400;

// Получаем все элементы списка
var listItems = document.querySelectorAll(".dropdown > li");

// Добавляем обработчики событий для каждого элемента списка
listItems.forEach(function(listItem) {
  listItem.addEventListener("mouseenter", function() {
    var container = this,
        list = container.querySelector("ul"),
        anchor = container.querySelector("a"),
        height = list.offsetHeight * 1.1, // make sure there is enough room at the bottom
        multiplier = height / maxHeight; // needs to move faster if list is taller

    // need to save height here so it can revert on mouseout
    container.dataset.origHeight = container.offsetHeight;

    // so it can retain it's rollover color all the while the dropdown is open
    anchor.classList.add("hover");

    // make sure dropdown appears directly below parent list item
    list.style.display = "block";
    list.style.paddingTop = container.dataset.origHeight + "px";

    // don't do any animation if list shorter than max
    if (multiplier > 1) {
      container.style.height = maxHeight + "px";
      container.style.overflow = "hidden";
      container.addEventListener("mousemove", function(e) {
        var offset = container.getBoundingClientRect(),
            relativeY = ((e.pageY - offset.top) * multiplier) - (container.dataset.origHeight * multiplier);
        if (relativeY > container.dataset.origHeight) {
          list.style.top = -relativeY + container.dataset.origHeight + "px";
        }
      });
    }
  });

  listItem.addEventListener("mouseleave", function() {
    var container = this,
        list = container.querySelector("ul"),
        el = container.querySelector("a");

    // put things back to normal
    container.style.height = container.dataset.origHeight + "px";
    list.style.top = 0;
    list.style.display = "none";
    el.classList.remove("hover");
  });
});