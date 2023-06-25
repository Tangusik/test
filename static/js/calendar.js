let cal = {
    sMon: true, // Неделя начинается в понедельник
    mName: ["Янв", "Фев", "Март", "Апр", "Май", "Июнь", "Июль", "Авг", "Сен", "Окт", "Ноя", "Дек"],
// КАЛЕНДАРНЫЕ ДАННЫЕ
    data: null,
    sDay: 0,
    sMth: 0,
    sYear: 0, // Текущий выбранный день, месяц, год
// ОБЩИЕ HTML-ЭЛЕМЕНТЫ
    hMth: null,
    hYear: null,
    hForm: null,
    hfHead: null,
    hfDate: null,
    hfTxt: null,
    hfDel: null, // форма события
// КАЛЕНДАРЬ НАЧАЛА
    init: () => {
// ПОЛУЧИТЬ + УСТАНОВИТЬ ОБЩИЕ ЭЛЕМЕНТЫ HTML
        cal.hMth = document.querySelector("#cal-mth");
        cal.hYear = document.querySelector("#cal-yr");
        cal.hForm = document.querySelector("#cal-event");
        cal.hfHead = document.querySelector("#evt-head");
        cal.hfDate = document.querySelector("#evt-date");
        cal.hfTxt = document.querySelector("#evt-details");
        cal.hfDel = document.querySelector("#evt-del");
        document.querySelector("#evt-close").onclick = cal.close;
        cal.hfDel.onclick = cal.del;
        cal.hForm.onsubmit = cal.save;
// ДАТА СЕЙЧАС
        let now = new Date(),
            nowMth = now.getMonth(),
            nowYear = parseInt(now.getFullYear());
// ДОБАВИТЬ ВЫБОР МЕСЯЦЕВ
        for (let i = 0; i < 12; i++) {
            let opt = document.createElement("option");
            opt.value = i;
            opt.innerHTML = cal.mName[i];
            if (i === nowMth) {
                opt.selected = true;
            }
            cal.hMth.appendChild(opt);
        }
        cal.hMth.onchange = cal.list;
// ДОБАВИТЬ ВЫБОР ГОДОВ (Диапазон 10 лет)
        for (let i = nowYear - 10; i <= nowYear + 10; i++) {
            let opt = document.createElement("option");
            opt.value = i;
            opt.innerHTML = i;
            if (i === nowYear) {
                opt.selected = true;
            }
            cal.hYear.appendChild(opt);
        }
        cal.hYear.onchange = cal.list;
// СТАРТ - ВЫВОДА КАЛЕНДАРЯ
        cal.list();
    },
// СОЗДАТЬ КАЛЕНДАРЬ НА ВЫБРАННЫЙ МЕСЯЦ
    list: () => {
// ОСНОВНЫЕ РАСЧЕТЫ - ДНИ В МЕСЯЦЕ, ДЕНЬ НАЧАЛА + КОНЕЦ
// Примечание. Январь равен 0, а декабрь — 11.
// Примечание. Воскресенье – 0, а суббота – 6.
        cal.sMth = parseInt(cal.hMth.value); // выбранный месяц
        cal.sYear = parseInt(cal.hYear.value); // выбранный год
        let daysInMth = new Date(cal.sYear, cal.sMth + 1, 0).getDate(), // количество дней в выбранном месяце
            startDay = new Date(cal.sYear, cal.sMth, 1).getDay(), // первый день месяца
            endDay = new Date(cal.sYear, cal.sMth, daysInMth).getDay(), // последний день месяца
            now = new Date(), // текущая дата
            nowMth = now.getMonth(), // текущий месяц
            nowYear = parseInt(now.getFullYear()), // текущий год
            nowDay = cal.sMth === nowMth && cal.sYear === nowYear ? now.getDate() : null;
// ЗАГРУЗИТЬ ДАННЫЕ ИЗ ЛОКАЛЬНОГО ХРАНИЛИЩА
        cal.data = localStorage.getItem("cal-" + cal.sMth + "-" + cal.sYear);
        if (cal.data == null) {
            localStorage.setItem("cal-" + cal.sMth + "-" + cal.sYear, "{}");
            cal.data = {};
        } else {
            cal.data = JSON.parse(cal.data);
        }


// Пустые квадраты перед началом месяца
        let squares = [];
        if (cal.sMon && startDay !== 1) {
            let blanks = startDay === 0 ? 7 : startDay;
            for (let i = 1; i < blanks; i++) {
                squares.push("b");
            }
        }
        if (!cal.sMon && startDay !== 0) {
            for (let i = 0; i < startDay; i++) {
                squares.push("b");
            }
        }
// Дни месяца
        for (let i = 1; i <= daysInMth; i++) {
            squares.push(i);
        }
// Пустые квадраты после окончания месяца
        if (cal.sMon && endDay !== 0) {
            let blanks = endDay === 6 ? 1 : 7 - endDay;
            for (let i = 0; i < blanks; i++) {
                squares.push("b");
            }
        }
        if (!cal.sMon && endDay !== 6) {
            let blanks = endDay === 0 ? 6 : 6 - endDay;
            for (let i = 0; i < blanks; i++) {
                squares.push("b");
            }
        }

// ВЫВЕСТИ HTML КАЛЕНДАРЬ
        let table = document.querySelector("#calendar");
// // Первая строка - названия дней
        let cRow = document.createElement("tr"),
            days = ["Вс", "пн", "Вт", "Ср", "Чт", "пт", "Сб"];
        if (cal.sMon) {
            days.push(days.shift());
        }
        for (let d of days) {
            let cCell = document.createElement("td");
            cCell.innerHTML = d;
            cRow.appendChild(cCell);
        }
        cRow.classList.add("head");
        table.appendChild(cRow);
// // Дни в месяце
        let total = squares.length;
        cRow = document.createElement("tr");
        cRow.classList.add("day");
        for (let i = 0; i < total; i++) {
            let cCell = document.createElement("td");
            if (squares[i] === "b") {
                cCell.classList.add("blank");
            } else {
                if (nowDay === squares[i]) {
                    cCell.classList.add("today");
                }
                cCell.innerHTML = `<div class="dd">${squares[i]}</div>`;
                if (cal.data[squares[i]]) {
                    cCell.innerHTML += "<div class='evt'>" + cal.data[squares[i]] + "</div>";
                }
                cCell.onclick = () => {
                    cal.show(cCell);
                };
            }
            cRow.appendChild(cCell);
            if (i !== 0 && (i + 1) % 7 === 0) {
                table.appendChild(cRow);
                cRow = document.createElement("tr");
                cRow.classList.add("day");
            }
        }
        cal.close();
    },
// // ПОКАЗАТЬ РЕДАКТИРОВАНИЕ СОБЫТИЙ ДЛЯ ВЫБРАННОГО ДНЯ
    show: (el) => {
// // ПОЛУЧИТЬ СУЩЕСТВУЮЩИЕ ДАННЫЕ
//         cal.sDay = el.getElementsByClassName("dd")[0].innerHTML;
//         let isEdit = cal.data[cal.sDay] !== undefined;
// // // ОБНОВИТЬ ФОРМУ МЕРОПРИЯТИЯ
//         cal.hfTxt.value = isEdit ? cal.data[cal.sDay] : "";
//         cal.hfHead.innerHTML = isEdit ? "РЕДАКТИРОВАТЬ МЕРОПРИЯТИЕ" : "ДОБАВИТЬ МЕРОПРИЯТИЕ";
//         cal.hfDate.innerHTML = `${cal.sDay} ${cal.mName[cal.sMth]} ${cal.sYear}`;
//         if (isEdit) {
//             cal.hfDel.classList.remove("ninja");
//         } else {
//             cal.hfDel.classList.add("ninja");
//         }
//         cal.hForm.classList.remove("ninja");
//     },
// // // ЗАКРЫТЬ СОБЫТИЕ
//     close: () => {
//         cal.hForm.classList.add("ninja");
//     },
// // // СОХРАНИТЬ СОБЫТИЕ
//     save: () => {
//         cal.data[cal.sDay] = cal.hfTxt.value;
//         localStorage.setItem(`cal-${cal.sMth}-${cal.sYear}`, JSON.stringify(cal.data));
//         cal.list();
//         return false;
//     },
// // // УДАЛИТЬ СОБЫТИЕ НА ВЫБРАННУЮ ДАТУ
//     del: () => {
//         if (confirm("Delete event?")) {
//             delete cal.data[cal.sDay];
//             localStorage.setItem(`cal-${cal.sMth}-${cal.sYear}`, JSON.stringify(cal.data));
//             cal.list();
//         }


    }
};
window.addEventListener("load", cal.init);