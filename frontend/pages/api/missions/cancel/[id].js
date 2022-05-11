import Cookies from 'cookies'

export default async function handler(req, res) {
    const { id } = req.query
    try {
        const cookies = new Cookies(req, res)
        const token = cookies.get('altJWT')
        const response = await fetch(`http://127.0.0.1:8000/missions/cancel_mission/${id}/`,
            {
                method: 'POST',
                headers: { 'Authorization': token }
            })
        console.log('cancel/[id]', response.json())
        res.status(200).json({ missions: response })
    } catch (error) {
        console.error(error)
        return res.status(error.status || 500).end(error.message)
    }

}