const input = document.getElementById('prescription-photo-input') as HTMLInputElement;
const button = document.getElementById('upload-action') as HTMLButtonElement;
const status = document.getElementById('upload-status') as HTMLParagraphElement;

button.addEventListener('click', () => {
    input.click();
});

input.addEventListener('change', () => {
    const file = input.files?.[0];
    status.textContent = file ? `Selected: ${file.name}` : '';
});
