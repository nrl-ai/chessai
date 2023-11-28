"use client"

import { useEffect, useRef, useState } from "react"
import { Button } from "@/registry/default/ui/button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/registry/default/ui/select"
import { useToast } from "@/registry/default/ui/use-toast"

import { DebugImages } from "@/components/debug-images"
import { NewGame } from "@/components/new-game"

const DotBgStyle = {
  backgroundImage: "radial-gradient(#888888 0.75px, transparent 0)",
  backgroundSize: "32px 32px",
  backgroundPosition: "-19px -19px",
  minHeight: "calc(100vh - 5rem)",
}

function LoadingIcon() {
  return (
    <div role="status inline-block">
      <svg
        aria-hidden="true"
        className="inline-block h-4 w-4 animate-spin fill-blue-600 text-gray-200 dark:text-gray-600"
        viewBox="0 0 100 101"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
          fill="currentColor"
        />
        <path
          d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
          fill="currentFill"
        />
      </svg>
      <span className="sr-only">Loading...</span>
    </div>
  )
}

export default function IndexPage() {
  const { toast } = useToast()
  const [selectedCamera, setSelectedCamera] = useState<Number>(0)
  const [cameraList, setCameraList] = useState<string[]>([])
  useEffect(() => {
    fetch("/api/camera/list")
      .then((res) => res.json())
      .then((data) => {
        setCameraList(data.available_camera_ports)
        setSelectedCamera(data.selected_camera_port)
      })
  }, [])
  function switchCamera(camera: string) {
    fetch("/api/camera/switch", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ camera_id: Number.parseInt(camera) }),
    })
      .then((res) => res.json())
      .then((data) => {
        setSelectedCamera(Number.parseInt(camera))
      })
  }
  function resetCamera() {
    fetch("/api/camera/reset", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    }).then((res) => res.json())
    setTimeout(() => {
      window.location.href = "/"
    }, 500)
  }

  const visualizationImage = useRef<HTMLImageElement>(null)

  // Refresh images every 1 second
  useEffect(() => {
    const interval = setInterval(() => {
      if (visualizationImage.current) {
        visualizationImage.current.src =
          "/api/vision/visualization_frame?t=" + Date.now()
      }
    }, 1000)
    return () => clearInterval(interval)
  }, [])

  const getHint = async () => {
    const hint = await fetch("/api/xiangqi/get_hint", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }).then((res) => res.json())
    if (hint.error) {
      toast({
        title: "Error",
        description: hint.error,
        duration: 3000,
      })
      return
    }
    toast({
      title: "Hint",
      description: `Best move: ${hint.best_move}`,
      duration: 3000,
    })
  }

  const [currentGame, setCurrentGame] = useState<any>({
    is_playing: false,
    next_player: "r",
  })
  useEffect(() => {
    fetch("/api/xiangqi/current_game", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then(setCurrentGame)
  }, [])
  const isRedTurn = currentGame.is_playing && currentGame.next_player === "r"
  const isBlackTurn =
    currentGame.is_playing && currentGame.next_player === "b"
  const isPlaying = currentGame.is_playing

  const play = async () => {
    const res = await fetch("/api/xiangqi/play", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    }).then((res) => res.json())
    if (res.error) {
      toast({
        title: "Error",
        description: res.error,
        duration: 3000,
      })
      return
    }
    if (!res.success) {
      toast({
        title: "Error",
        description: res.message || "Unknown error",
        duration: 3000,
      })
      return
    }
  }

  return (
    <div style={DotBgStyle} className="pt-6">
      <section className="container flex flex-row gap-8 py-2">
        <div className="flex w-[250px] flex-col gap-4">
          <h2 className="text-xl font-semibold leading-none">Board Camera</h2>
          <img
            src="/api/vision/original_frame"
            className="rounded-md"
            width={320}
            height={240}
            alt="Viz Image"
          />
          <Select
            onValueChange={(value) => switchCamera(value)}
            value={selectedCamera.toString()}
          >
            <SelectTrigger id="camera">
              <SelectValue placeholder="Select Camera">
                Camera:&nbsp;{selectedCamera.toLocaleString()}
              </SelectValue>
            </SelectTrigger>
            <SelectContent position="popper">
              {cameraList.map((camera) => (
                <SelectItem value={camera} key={camera}>
                  Camera:&nbsp;{camera}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button
            className="w-full"
            onClick={() => {
              resetCamera()
            }}
          >
            Reset Camera
          </Button>
          <div>
            Visualization of current board camera. Please make sure the board is
            in the center of the camera and all ARUCO markers are visible.
          </div>
        </div>
        <div className="flex flex-col gap-2">
          <img
            ref={visualizationImage}
            src="/api/vision/visualization_frame"
            className="w-full max-w-[500px] rounded-md"
            width={500}
            height={500}
            alt="Viz Image"
          />
        </div>
        <div className="flex w-[250px] flex-col gap-2">
          <div className="flex flex-row gap-2">
            <div className="flex flex-col gap-1">
              <div className={"text-xl flex" + (isRedTurn ? " font-bold" : "")}>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth="1.5"
                  stroke="currentColor"
                  className="mr-1 h-6 w-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"
                  />
                </svg>
                Red &nbsp;
                {isRedTurn && <LoadingIcon />}
              </div>
              <div className="text-xl">-------------</div>
            </div>
            <div className="flex flex-col gap-1">
              <div
                className={"text-xl flex" + (isBlackTurn ? " font-bold" : "")}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  className="ml-1 h-6 w-6"
                >
                  <path
                    fillRule="evenodd"
                    d="M7.5 6a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM3.751 20.105a8.25 8.25 0 0116.498 0 .75.75 0 01-.437.695A18.683 18.683 0 0112 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 01-.437-.695z"
                    clipRule="evenodd"
                  />
                </svg>
                Black &nbsp;
                {isBlackTurn && <LoadingIcon />}
              </div>
              <div className="text-xl">-------------</div>
            </div>
          </div>
          <Button className="h-20 w-full bg-blue-600 hover:bg-blue-500 dark:text-white"
            onClick={play}
            disabled={!isPlaying}
          >
            Play (Space)
          </Button>
          <NewGame>
            <Button className="w-full">New Game</Button>
          </NewGame>
          <Button className="w-full" onClick={getHint} disabled={!isPlaying}>
            Hint
          </Button>
          <Button className="w-full" disabled={!isPlaying}>
            AI Analyzer
          </Button>
          {!isPlaying && (
            <div className="text-sm text-gray-500 dark:text-gray-400">
              Click <b>New Game</b> to start a new game from current position.
            </div>
          )}
          <div className={"hidden flex-col gap-2" + (isPlaying ? "" : " hidden")}>
            <h2 className="mt-4 text-xl font-semibold leading-none">
              Move History
            </h2>
            <div className="max-h-[100px] w-full overflow-y-auto">
              <table className="flex flex-col gap-1">
                <thead className="border-b-2 border-gray-600">
                  <tr className="flex flex-row gap-1 text-left">
                    <th className="w-1/2">ID</th>
                    <th className="w-1/2">Move</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="flex flex-row gap-1">
                    <td className="w-1/2">1</td>
                    <td className="w-1/2">e2e4</td>
                  </tr>
                  <tr className="flex flex-row gap-1">
                    <td className="w-1/2">2</td>
                    <td className="w-1/2">e7e5</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>
      <section className="container mt-4 grid items-center gap-2 py-2">
        <DebugImages />
      </section>
    </div>
  )
}
