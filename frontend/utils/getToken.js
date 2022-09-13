import Cookies from 'cookies'

function getTokenCookie(res, req) {
    const cookies = new Cookies(req, res)
    try {
      return cookies.get('altJWT')
    } catch (e) {
      return null
    }
  }


export default getTokenCookie