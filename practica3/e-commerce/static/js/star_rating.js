document.addEventListener('DOMContentLoaded', () => {
	const span_para_estrellas = document.querySelectorAll('span.sp');

	span_para_estrellas.forEach((ele) => {
		const id = ele.getAttribute('data-id');
		draw_star_by_id(id, ele);
		puntuar(ele);
	});


	function puntuar(ele) {
		ele.querySelectorAll('.fa').forEach((star) => {
			star.addEventListener('click', (event) => {
				const puntuacion = parseInt(event.target.dataset.index) + 1;
				console.log(`La valoración ha sido de: ${puntuacion}`);

				const elemento_id = ele.getAttribute('data-id');
				fetch(`http://localhost:8000/api/productos/${elemento_id}/${puntuacion}`, { method: 'PUT' })
					.then(response => response.json())
					.then(() => {
						draw_star_by_id(elemento_id, ele);
					})
					.catch(error => {
						console.error('Error al realizar la solicitud PUT:', error);
					});
			});


			star.addEventListener('mouseover', (event) => {
				const index = parseInt(event.target.dataset.index);
				const stars = ele.querySelectorAll('.fa');

				stars.forEach((star, i) => {
					if (i <= index) {
						star.classList.add('checked');
					} else {
						star.classList.remove('checked');
					}
				});
			});

			star.addEventListener('mouseout', (event) => {
				const stars = ele.querySelectorAll('.fa');

				stars.forEach((star) => {
					star.classList.remove('checked');
				});
			});
		});
	}

	function draw_star_by_id(id, ele) {
		fetch(`http://localhost:8000/api/productos/${id}`)
			.then(response => response.json())
			.then(data => {
				const rate = data.rating.rate;
				const count = data.rating.count;
				let num_star = 0;
				let max_star = 5

				ele.innerHTML = ''; // Clear the previous stars

				for (let i = 1; i <= rate; i++) {
					ele.innerHTML += `<span class="fa fa-star" data-index="${num_star}"></span>`;
					num_star++;
				}

				if (rate % 1 >= 0.5) {
					ele.innerHTML += `<span class="fa fa-star-half-o" data-index="${num_star}"></span>`;
					num_star++;
				}

				let last_stars = max_star - num_star;
				for (let i = 0; i < last_stars; i++) {
					ele.innerHTML += `<span class="fa fa-star-o" data-index="${num_star}"></span>`;
					num_star++;
				}

				ele.innerHTML += `<span class="rate">(${Number((rate).toFixed(1))}),  ${count})</span>`;

				puntuar(ele); // Add event listeners to the newly drawn stars
			});
	}

	function handleStarClick(starIndex) {
		console.log('Número del elemento seleccionado:', starIndex);
	}
});
