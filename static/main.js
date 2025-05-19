document.addEventListener('DOMContentLoaded', function() {
    const responseBox = document.getElementById('response-box');

    const amazonModal = document.getElementById('amazon-modal');
    if (amazonModal) {
        amazonModal.style.display = 'flex';
    }

    const ctaForm = document.getElementById('cta-offers-form');
    if (ctaForm) {
        ctaForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const nameInput = ctaForm.querySelector('#cta-name');
            const phoneInput = ctaForm.querySelector('#cta-phone');
            const emailInput = ctaForm.querySelector('#cta-email');

            let isValid = true;
            let errorMessage = '';

            const phoneValue = phoneInput.value.replace(/\D/g, '');

            if ((phoneValue.length !== 10 && phoneValue.length !== 11) || !/^\d+$/.test(phoneValue)) {
                isValid = false;
                errorMessage += 'Telefone inválido. Use o formato DDD (2 dígitos) + 8 ou 9 dígitos.\n';
                phoneInput.focus();
            }

            const emailValue = emailInput.value;

            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailValue)) {
                isValid = false;
                errorMessage += 'Email inválido. Verifique o formato (ex: usuario@dominio.com).\n';
                if (isValid) emailInput.focus();
            }

            if (!isValid) {
                // Show error in responseBox instead of alert for better UX
                responseBox.textContent = errorMessage.trim();
                responseBox.style.color = 'red';
                return;
            }

            const formData = new FormData(ctaForm);

            fetch(ctaForm.action, {
                method: 'POST',
                body: formData,
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errData => {
                        throw new Error(errData.message || 'Ops. Network response not ok.');
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    responseBox.textContent = 'Cadastro realizado com sucesso!';
                    responseBox.style.color = 'green';

                    setTimeout(() => {
                        window.location.reload();
                    }, 5000);
                } else {
                    responseBox.textContent = data.message || 'Ocorreu um erro ao processar o cadastro.';
                    responseBox.style.color = 'red';
                }
            })
            .catch(error => {
                console.error('Erro ao submeter o formulário:', error);
                responseBox.textContent = 'Erro ao submeter o formulário: ' + error.message;
                responseBox.style.color = 'red';
            });
        });
    }
});
