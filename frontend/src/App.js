import axios from 'axios';
import { useState } from 'react';
import './App.css';
import config from "./config.js"
import urlJoin from 'url-join';

function App () {
  const [highlight, setHighlight] = useState(true)
  const [templateName, setTemplateName] = useState("HUST")
  const [markdownFile, setMarkdownFile] = useState(null);
  const [errorToastVisible, setErrorToastVisible] = useState(false)
  const [errorToast, setErrorToast] = useState("")

  const showError = (msg, duration) => {
    setErrorToast(msg)
    setErrorToastVisible(true)
    setTimeout(() => {
      setErrorToastVisible(false)
    }, duration);
  }

  const submitGenerateTask = () => {
    const formData = new FormData()
    formData.append("file", markdownFile)
    formData.append("template", templateName)
    formData.append("highlight", highlight)
    axios.post(config.TASKS_URL, formData)
      .then((resp) => {
        const task_id = resp.data.task_id
        const interval = setInterval(() => {
          // poll the status of task
          axios.get(urlJoin(config.TASKS_URL, task_id, config.TASKS_STATUS_SUFFIX)).then((resp) => {
            if (resp.data.status === "PENDING") return
            clearInterval(interval);
            // download file
            axios.get(urlJoin(config.TASKS_URL, task_id), { responseType: 'blob' }).then((resp) => {
              const href = URL.createObjectURL(resp.data)
              const link = document.createElement('a')
              link.href = href
              link.setAttribute('download', 'output.docx')
              document.body.appendChild(link)
              link.click()
              document.body.removeChild(link)
              URL.revokeObjectURL(href)
            }).catch((err) => {
              console.log(err)
              if (err.response.data.detail) {
                showError(err.response.data.detail, 5000)
              } else {
                showError("download file failed", 5000)
              }
            })
          }).catch((err) => {
            if (err.response.data.detail) {
              showError(err.response.data.detail, 5000)
            } else {
              showError("get task status file failed", 5000)
              clearInterval(interval)
            }
          })
        }, 1000);
      })
  }

  return (
    <div data-theme="light" className="grid grid-col-1">
      <header>
        <div className="navbar bg-primary text-primary-content">
          <a href="/" className="btn btn-ghost normal-case text-2xl">md2docx</a>
        </div>
      </header>
      <div className={"toast toast-top toast-end "}>
        <div className={"transition-opacity ease-in-out duration-1000 alert alert-error " + (errorToastVisible ? "opacity-100" : "opacity-0")}>
          <div>
            <span>{errorToast}</span>
          </div>
        </div>
      </div>
      <div className="grid grid-cols-12 gap-4 mt-6 h-full">
        <div className="col-start-4 col-span-6 place-item-center mb-8">
          <p className="text-5xl text-primary text-center font-bold font-mono">No More Docx Reports!</p>
          <p className="text-2xl text-primary text-center font-slim font-sans mt-2">generate your reports in seconds</p>
        </div>

        <div className="col-start-3 col-end-4 justify-self-end self-center">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" className="bi bi-1-circle-fill fill-primary" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0ZM9.283 4.002V12H7.971V5.338h-.065L6.072 6.656V5.385l1.899-1.383h1.312Z" />
          </svg>
        </div>
        <div className="col-start-4 col-end-10 self-center">
          <span className="text-xl text-primary">
            Chose your markdown file (or zip file)
            <div className="tooltip ml-4" data-tip="Please read manual first">
              <a href="/">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-question-circle inline-block fill-secondary" viewBox="0 0 16 16">
                  <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z" />
                  <path d="M5.255 5.786a.237.237 0 0 0 .241.247h.825c.138 0 .248-.113.266-.25.09-.656.54-1.134 1.342-1.134.686 0 1.314.343 1.314 1.168 0 .635-.374.927-.965 1.371-.673.489-1.206 1.06-1.168 1.987l.003.217a.25.25 0 0 0 .25.246h.811a.25.25 0 0 0 .25-.25v-.105c0-.718.273-.927 1.01-1.486.609-.463 1.244-.977 1.244-2.056 0-1.511-1.276-2.241-2.673-2.241-1.267 0-2.655.59-2.75 2.286zm1.557 5.763c0 .533.425.927 1.01.927.609 0 1.028-.394 1.028-.927 0-.552-.42-.94-1.029-.94-.584 0-1.009.388-1.009.94z" />
                </svg>
              </a>
            </div>
          </span>
        </div>
        <div className="col-start-4 col-end-12 place-item-center mb-8">
          <input type="file" className="file-input file-input-bordered file-input-primary w-full max-w-xs"
            onChange={(e) => setMarkdownFile(e.target.files[0])} />
        </div>

        <div className="col-start-3 col-end-4 justify-self-end self-center">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" className="bi bi-2-circle-fill fill-primary" viewBox="0 0 16 16">
            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0ZM6.646 6.24c0-.691.493-1.306 1.336-1.306.756 0 1.313.492 1.313 1.236 0 .697-.469 1.23-.902 1.705l-2.971 3.293V12h5.344v-1.107H7.268v-.077l1.974-2.22.096-.107c.688-.763 1.287-1.428 1.287-2.43 0-1.266-1.031-2.215-2.613-2.215-1.758 0-2.637 1.19-2.637 2.402v.065h1.271v-.07Z" />
          </svg>
        </div>
        <div className="col-start-4 col-end-10 self-center">
          <span className="text-xl text-primary">Set generate options</span>
        </div>
        <div className="col-start-4 col-end-12 place-item-center">
          <label className="label">
            <span className="label-text">Chose a template</span>
          </label>
          <select className="select select-primary w-full max-w-xs" onChange={(value) => {
            setTemplateName(value.target.value)
          }}>
            <option selected key="hust">HUST</option>
          </select>
        </div>
        <div className="col-start-4 col-end-12 place-item-center mb-8">
          <label className="flex items-top cursor-pointer">
            <input type="checkbox" className="checkbox checkbox-primary" style={{ "margin-top": "2px" }}
              checked={highlight}
              onChange={(value) => {
                setHighlight(value.target.checked)
              }} />
            <span className="text-xl text-primary ml-4">Code Hightlight</span>
          </label>
        </div>

        <div className="col-start-3 col-end-4 justify-self-end self-center">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" className="bi bi-3-circle-fill fill-primary" viewBox="0 0 16 16">
            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0Zm-8.082.414c.92 0 1.535.54 1.541 1.318.012.791-.615 1.36-1.588 1.354-.861-.006-1.482-.469-1.54-1.066H5.104c.047 1.177 1.05 2.144 2.754 2.144 1.653 0 2.954-.937 2.93-2.396-.023-1.278-1.031-1.846-1.734-1.916v-.07c.597-.1 1.505-.739 1.482-1.876-.03-1.177-1.043-2.074-2.637-2.062-1.675.006-2.59.984-2.625 2.12h1.248c.036-.556.557-1.054 1.348-1.054.785 0 1.348.486 1.348 1.195.006.715-.563 1.237-1.342 1.237h-.838v1.072h.879Z" />
          </svg>
        </div>
        <div className="col-start-4 col-end-8 self-center">
          <span className="text-xl text-primary">Get your docx report</span>
        </div>
        <div className="col-start-4 col-end-12 place-item-center" onClick={submitGenerateTask}>
          <button className="btn btn-primary">Generate</button>
        </div>

      </div>
    </div >
  );
}

export default App;
