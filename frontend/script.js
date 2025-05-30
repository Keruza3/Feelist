document.addEventListener('DOMContentLoaded', () => {
  const formulario = document.getElementById('chat-form');
  const campoTexto = document.getElementById('texto-usuario');
  const contenedorRespuesta = document.getElementById('response-box');

  formulario.addEventListener('submit', async (evento) => {
    evento.preventDefault();

    const mensajeUsuario = campoTexto.value.trim();
    if (!mensajeUsuario) return;

    contenedorRespuesta.innerText = "Procesando... probablemente contra mi voluntad.";

    try {
      const respuesta = await fetch('https://feelist.onrender.com/api/monday', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: mensajeUsuario })
      });

      if(!respuesta.ok) {
        trow new error(`Error el servidor: ${mensajeUsuario}`);
      
      const datos = await respuesta.json();
      const { mood, quote, tracks } = datos;

      // Verificamos que tracks exista y sea un array
      if (!Array.isArray(tracks)) {
        throw new Error("La respuesta no contiene una lista válida de canciones.");
      }

      contenedorRespuesta.innerHTML = `
        <div class="respuesta-container">
          <h5 class="respuesta-titulo">Mood detectado:</h5>
          <p class="respuesta-mood">${mood}</p>

          <h6 class="respuesta-titulo">Frase de Monday:</h6>
          <blockquote class="respuesta-quote">"${quote}"</blockquote>

          <h6 class="respuesta-titulo">Recomendación musical:</h6>
          <ul class="respuesta-lista">
            ${tracks.map(cancion => `
              <li class="respuesta-item">${cancion.title} – ${cancion.artist}</li>
            `).join('')}
          </ul>
        </div>
      `;

    } catch (error) {
      contenedorRespuesta.innerText = "Error existencial. Monday no puede ayudarte ahora.";
      console.error("Error detectado en el cliente:", error);
    }

    campoTexto.value = '';
  });
});
