
import { useState } from 'react'
import { useRouter } from 'next/router'

function Login(res, req) {
    const router = useRouter();
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [areCredentialsWrong, setareCredentialsWrong] = useState(false)
    const submitAuth = async () => {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password }),
            headers: {
                'Content-Type': 'application/json',
            },
        })
        console.log(response.status)
        if (response.status == 200) {
            router.push('/')
        }
        else {
            setareCredentialsWrong(true)
            return {}
        }
    }
    return (

        <div className={`h-full w-full flex items-center justify-center`} style={{ zIndex: 1 }}>
            <form className="self-center bg-transparent	 shadow-md rounded">
                {areCredentialsWrong ? <p className="text-center text-red-300 text-xl italic ">Wrong credentials!</p> : <></>}
                <div className="mb-4">
                    <label className="block text-white text-sm font-bold mb-2" htmlFor="username">
                        Username
                    </label>
                    <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="Username" value={username} onChange={e => { setUsername(e.currentTarget.value); }} ></input>
                </div>
                <div className="mb-6">
                    <label className="block text-white text-sm font-bold mb-2" htmlFor="password">
                        Password
                    </label>
                    <input className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" id="password" type="password" placeholder="******************" value={password} onChange={e => { setPassword(e.currentTarget.value); }}></input>
                </div>
                <div className="flex items-center justify-between">
                    <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button" onClick={submitAuth}>
                        Sign In
                    </button>
                    <a className="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800" href="#">
                        Forgot Password?
                    </a>
                </div>
            </form>
        </div>
    )
}

export default Login;