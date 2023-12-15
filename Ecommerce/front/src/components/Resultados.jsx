import React from 'react'

export default function Resultados({productos}) {
  return ( // iria el comnponente del react
    <ul>
        {productos.map((producto) => (
            <li key={producto.id} >{producto.title}</li>
        ))}

    </ul>
  )
}
