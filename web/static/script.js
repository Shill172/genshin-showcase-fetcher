generateBtn.addEventListener("click", async function () {
    const uid = uidInput.value;

    const checkboxes = document.querySelectorAll('#showcase-form input[type="checkbox"]');
    const selectedFields = [];

    checkboxes.forEach(function (checkbox) {
        if (checkbox.checked) {
            selectedFields.push(checkbox.value);
        }
    });

    const response = await fetch("/showcase", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            uid: uid,
            fields: selectedFields
        })
    });

    const data = await response.json();

    console.log("Got data back:", data);
});