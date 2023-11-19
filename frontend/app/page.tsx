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

import { DebugImages } from "@/components/debug-images"

const DotBgStyle = {
  backgroundImage: "radial-gradient(#888888 0.75px, transparent 0)",
  backgroundSize: "32px 32px",
  backgroundPosition: "-19px -19px",
  minHeight: "calc(100vh - 5rem)",
}

export default function IndexPage() {
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
          "/api/xiangqi/visualization_frame?t=" + Date.now()
      }
    }, 1000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div style={DotBgStyle} className="pt-6">
      <section className="container flex flex-row gap-8 py-2">
        <div className="flex w-[250px] flex-col gap-4">
          <h2 className="text-xl font-semibold leading-none">Board Camera</h2>
          <img
            src="/api/xiangqi/original_frame"
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
            src="/api/xiangqi/visualization_frame"
            className="w-full max-w-[500px] rounded-md"
            width={500}
            height={500}
            alt="Viz Image"
          />
        </div>
        <div className="flex w-[200px] flex-col gap-2">
          <div className="flex flex-row gap-2">
            <div className="flex flex-col gap-1">
              <div className="text-sm">Player 1</div>
              <div className="text-2xl">00:00:00</div>
            </div>
            <div className="flex flex-col gap-1">
              <div className="text-sm">Player 2</div>
              <div className="text-2xl">00:00:00</div>
            </div>
          </div>
          <Button className="h-20 w-full bg-blue-600 hover:bg-blue-500 dark:text-white">
            Play (Space)
          </Button>
          <Button className="w-full">New Game</Button>
          <Button className="w-full">Move Suggestion</Button>
          <Button className="w-full">Analyze Match</Button>
          <Button className="w-full">Save History</Button>
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
      </section>
      <section className="container mt-4 grid items-center gap-2 py-2">
        <DebugImages />
      </section>
    </div>
  )
}
