// se ejecuta recien cargada la página

document.addEventListener('DOMContentLoaded', () => {
	// donde se inyecte el código html
	const span_para_estrellas = document.querySelectorAll('span.sp') 

	span_para_estrellas.forEach((ele) => {   // arrow function
		// comillas hacia atrás: es6 multiline
		// conectar con el api para recoger el rating y ponerlo
		// busca el resultado según el id de cada elemento y encuentra el rating de cada uno
		const id = ele.getAttribute('data-id');
		fetch(`http://localhost:8000/api/productos/${id}`)
			.then(response => response.json())
			.then(data => {
				const rate = data.rating.rate;
				const count = data.rating.count;
				let num_star=0;
								
				for (let i = 1; i <= rate; i++) {
					ele.innerHTML += `<span class="fa fa-star checked"></span>`;
					num_star++;
				}

				console.log(rate % 1)
				if (rate % 1 >= 0.5) {
					ele.innerHTML += `<span class="fa fa-star-half-o checked"></span>`;
					num_star++;
				}

				for (let i = 1; i <= 5 - num_star; i++) {
					ele.innerHTML += `<span class="fa fa-star-o checked"></span>`;
				}
			})
	})
})

