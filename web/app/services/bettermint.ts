

export const createLinkToken = async () => {
    const response = await fetch('http://localhost:5000/create_link_token', { method: 'POST' });
    const { link_token } = await response.json();
    return link_token
};
