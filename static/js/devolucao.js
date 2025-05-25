// Variáveis globais do carrossel
let imagensCarrossel = [];
let indiceAtual = 0;

// Abrir modal com imagens do carrossel
async function verImagens(id) {
  try {
    const response = await fetch(`/imagens_devolucao/${id}`);
    if (!response.ok) throw new Error('Erro ao buscar imagens.');

    const data = await response.json();
    imagensCarrossel = data.imagens || [];

    if (imagensCarrossel.length === 0) {
      alert('Nenhuma imagem disponível.');
      return;
    }

    indiceAtual = 0;
    atualizarImagemCarrossel();
    document.getElementById('modal-carrossel').style.display = 'block';
  } catch (error) {
    alert(error.message);
  }
}

// Atualiza imagem exibida no carrossel
function atualizarImagemCarrossel() {
  const imgElement = document.getElementById('carousel-image');
  let imagemRelativa = imagensCarrossel[indiceAtual];

  // Remove prefixo 'imagens/' se existir
  if (imagemRelativa.startsWith('imagens/')) {
    imagemRelativa = imagemRelativa.replace('imagens/', '');
  }

  imgElement.src = `${window.location.origin}/static/imagens/${imagemRelativa}`;
  imgElement.alt = `Imagem ${indiceAtual + 1} de ${imagensCarrossel.length}`;
  atualizarIndicador();
}

// Atualiza indicador de posição no carrossel
function atualizarIndicador() {
  const indicador = document.getElementById('carousel-indicador');
  if (indicador) {
    indicador.textContent = `${indiceAtual + 1} / ${imagensCarrossel.length}`;
  }
}

// Botão de fechar modal
document.getElementById('close-modal').onclick = () => {
  document.getElementById('modal-carrossel').style.display = 'none';
};

// Fechar modal clicando fora da imagem
document.getElementById('modal-carrossel').onclick = (e) => {
  if (e.target.id === 'modal-carrossel') {
    document.getElementById('modal-carrossel').style.display = 'none';
  }
};

// Botão de imagem anterior
document.getElementById('prev-btn').onclick = () => {
  if (imagensCarrossel.length > 0) {
    indiceAtual = (indiceAtual - 1 + imagensCarrossel.length) % imagensCarrossel.length;
    atualizarImagemCarrossel();
  }
};

// Botão de próxima imagem
document.getElementById('next-btn').onclick = () => {
  if (imagensCarrossel.length > 0) {
    indiceAtual = (indiceAtual + 1) % imagensCarrossel.length;
    atualizarImagemCarrossel();
  }
};

// Mover item para estoque físico
async function moverParaEstoqueFisico(id) {
  try {
    const res = await fetch('/mover_estoque_fisico', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id })
    });
    if (!res.ok) throw new Error("Erro ao mover para o estoque físico.");
    location.reload();
  } catch (error) {
    alert(error.message);
  }
}

// Mover item para descarte
async function moverParaDescarte(id) {
  console.log('ID recebido:', id);
  if (id === undefined) {
    alert('ID indefinido recebido!');
    return;
  }

  try {
    const res = await fetch(`/mover_para_descarte/${id}`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Erro ao mover para descarte.');
    location.reload();
  } catch (error) {
    alert(error.message);
  }
}

fetch('/mover_para_descarte/3', { method: 'POST' })
  .then(r => console.log(r.status))
  .catch(e => console.error(e));

// Função debounce para otimizar filtro de busca
function debounce(fn, delay) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

// Filtro em tempo real dos cards
const filtroInput = document.getElementById('filtro');
filtroInput.addEventListener('input', debounce(() => {
  const filtro = filtroInput.value.toLowerCase().trim();
  const cards = document.querySelectorAll('.card');

  cards.forEach(card => {
    const nome = card.getAttribute('data-nome').toLowerCase();
    card.style.display = nome.includes(filtro) ? '' : 'none';
  });
}, 300));

// Impede submissão ao pressionar Enter no campo de filtro
filtroInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') e.preventDefault();
});
