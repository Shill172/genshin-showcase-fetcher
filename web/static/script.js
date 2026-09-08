const generateBtn = document.getElementById("generate-btn");
const uidInput = document.getElementById("uid-input");

const fieldLabels = {
    level: "Lv.{}",
    constellation: "C{}",
    weapon: "{}",
    artifact_set: "{}",
    friendship: "FLv.{}",
    talents: "Talents {}",
    hp: "HP {}",
    atk: "ATK {}",
    defense: "DEF {}",
    crit: "CRIT {}",
    er: "ER {}",
    em: "EM {}",
    dmg_bonus: "{}"
};

function formatCharacterLine(character) {
    const parts = [character.name];

    for (const field in fieldLabels) {
        if (character[field] !== undefined) {
            const label = fieldLabels[field];
            const value = character[field];
            parts.push(label.replace("{}", value));
        }
    }

    return parts.join(", ");
}

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

    const lines = data.characters.map(formatCharacterLine);
    const previewText = lines.join("\n");

    document.getElementById("preview-box").value = previewText;

    console.log("Got data back:", data);
});