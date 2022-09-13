import Cookies from 'cookies'

export default async function handler(req, res) {
    try {
        const cookies = new Cookies(req, res)
        const token = cookies.get('altJWT')
        const response = await fetch('http://127.0.0.1:8000/characters/user_character/',
            {
                method: 'GET',
                headers: { 'Authorization': token }
            }).then(response => response.json())
        res.status(200).json({ character: response })
    } catch (error) {
        console.error(error)
        return res.status(error.status || 500).end(error.message)
    }

}
