import Cookies from 'cookies'

export default async function handler(req, res) {
    const cookies = new Cookies(req, res)
    const {username, password} = req.body
    try{
      const response = await fetch('http://127.0.0.1:8000/api-token-auth/', {
         method:'POST',
         body: JSON.stringify({'username':username, 'password':password}),
         headers: {
            'Content-Type': 'application/json'
          },
      }).then(response => response.json())
        if (response.token) {
          cookies.set('altJWT', 'Token ' + response.token)
          res.status(200).json({message: "Login Success!"})
        } else {
          res.status(401).json({message: "Login Failed"})
        }
        
     } catch (error) {
        console.error(error)
        return res.status(error.status || 500).end(error.message)
      }
    }