// Worker for static site hosting
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const url = new URL(request.url);
  let path = url.pathname;
  
  // Add index.html for root paths
  if (path.endsWith('/')) {
    path += 'index.html';
  }
  
  // Try to fetch the asset
  try {
    const response = await fetch(`file://${path}`);
    return response;
  } catch (e) {
    // Return 404 if not found
    return new Response('Not found', {
      status: 404,
      headers: {
        'content-type': 'text/plain; charset=UTF-8'
      }
    });
  }
}
