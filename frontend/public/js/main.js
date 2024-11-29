// Example of basic interactivity
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            alert(`You clicked ${button.innerText}`);
        });
    });
});
