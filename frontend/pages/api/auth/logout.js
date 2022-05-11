import Cookies from 'cookies'

export default async function handler(req, res) {
    const cookies = new Cookies(req, res)
    cookies.set('altJWT', 'none')
    res.status(200).json({message: "Logout Success!"})
}
