function syncDropdowns(first, second) {
    let options = $(second).find('option');
    for (let option of options) {
        option.disabled = option.value == first.value;
    }
}

$("#erste_Vertiefung").change((evt) => {
    syncDropdowns(evt.target, $('#zweite_Vertiefung'));
});

$("#zweite_Vertiefung").change((evt) => {
    syncDropdowns(evt.target, $('#erste_Vertiefung'));
});

syncDropdowns($('#erste_Vertiefung'), $('#zweite_Vertiefung'));
