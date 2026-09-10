const generateBtn = document.getElementById("generate-btn");
const uidInput = document.getElementById("uid-input");
const showcaseForm = document.getElementById("showcase-form");
const previewBox = document.getElementById("preview-box");
const statusMessage = document.getElementById("status-message");

let fetchedCharacters = null; 

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

const allFields = Object.keys(fieldLabels);

const exampleCharacter = {
    name: "Amber",
    level: 90,
    constellation: 6,
    weapon: "R2 Skyward Harp",
    artifact_set: "2pc Bloodstained Chivalry + 2pc Pale Flame",
    friendship: 10,
    talents: "10/13/13",
    hp: 13478,
    atk: 998,
    defense: 738,
    crit: "70.0%/140.0%",
    er: "112.5%",
    em: 0,
    dmg_bonus: "Physical DMG 108.3%"
};

function formatCharacterLine(character, selectedFields) {
    const parts = [character.name];

    for (const field of selectedFields) {
        if (character[field] !== undefined) {
            const label = fieldLabels[field];
            const value = character[field];
            parts.push(label.replace("{}", value));
        }
    }

    return parts.join(", ");
}

function getSelectedFields() {
    const checkboxes = document.querySelectorAll('#showcase-form input[type="checkbox"]');
    const selectedFields = [];
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            selectedFields.push(checkbox.value);
        }
    });
    return selectedFields;
}

function updatePreview() {
    const selectedFields = getSelectedFields(); 
    const charactersToDisplay = fetchedCharacters || [exampleCharacter];

    const lines = charactersToDisplay.map(char => formatCharacterLine(char, selectedFields));

    previewBox.value = lines.join("\n");
}

showcaseForm.addEventListener("change", function (event) {
    if (event.target.type === "checkbox") {
        updatePreview();
    }
});

generateBtn.addEventListener("click", async function () {
    generateBtn.disabled = true;
    
    const uid = uidInput.value.trim();

    if (!isValidUid(uid)) {
        alert("Please enter a valid UID (9 or 10 digits, numbers only)");
        generateBtn.disabled = false;
        return;
    }

    // Send ALL field keys to the backend so it returns complete data
    const allFields = Object.keys(fieldLabels);

    statusMessage.textContent = "Fetching showcase...";

    try {
        const response = await fetch("/showcase", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                uid: uid,
                fields: allFields // Always request all fields
            })
        });

        const data = await response.json();

        if (!response.ok) {
            statusMessage.textContent = data.detail || "Something went wrong.";
            statusMessage.className = "error";
            return;
        }

        fetchedCharacters = data.characters;
        updatePreview(); // Correctly formats based on currently checked boxes
        statusMessage.textContent = "";
        statusMessage.className = "";

    } catch (error) {
        statusMessage.textContent = "Could not reach the server.";
        statusMessage.className = "error";

    } finally {
        generateBtn.disabled = false;
    }
});


function isValidUid(uid) {
    return /^\d{9,10}$/.test(uid);
}


updatePreview(); 