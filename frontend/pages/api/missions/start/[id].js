import Cookies from 'cookies'

export default async function handler(req, res) {
    const { id } = req.query
    console.log(`http://127.0.0.1:8000/missions/start_mission/${id}/`)
    try {
        const cookies = new Cookies(req, res)
        const token = cookies.get('altJWT')
        const response = await fetch(`http://127.0.0.1:8000/missions/start_mission/${id}/`,
            {
                method: 'POST',
                headers: { 'Authorization': token }
            })
        res.status(200).json({ missions: response })
    } catch (error) {
        console.error(error)
        return res.status(error.status || 500).end(error.message)
    }

}
