"use client"

import { useEffect, useRef, useState } from "react"
import { Button } from "@/registry/default/ui/button"
import { Checkbox } from "@/registry/default/ui/checkbox"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/registry/default/ui/select"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/registry/default/ui/table"

import { DebugImages } from "@/components/debug-images"

const DotBgStyle = {
  backgroundImage: "radial-gradient(#888888 0.75px, transparent 0)",
  backgroundSize: "32px 32px",
  backgroundPosition: "-19px -19px",
}

export default function IndexPage() {
  const visualizationImage = useRef<HTMLImageElement>(null)
  const originalImage = useRef<HTMLImageElement>(null)

  // Refresh images every 1 second
  useEffect(() => {
    const interval = setInterval(() => {
      if (visualizationImage.current) {
        visualizationImage.current.src =
          "/api/xiangqi/visualization_frame?" + Date.now()
      }
      if (originalImage.current) {
        originalImage.current.src = "/api/xiangqi/original_frame?" + Date.now()
      }
    }, 1000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div style={DotBgStyle} className="min-h-screen pt-6">
      <section className="container flex flex-row gap-6 py-2">
        <div className="flex w-[250px] flex-col gap-2">
          <h2 className="text-xl font-semibold leading-none">Camera</h2>
          <img
            ref={originalImage}
            src="/api/xiangqi/original_frame"
            className="rounded-md"
            width={320}
            height={240}
            alt="Viz Image"
          />
          <Select>
            <SelectTrigger id="camera">
              <SelectValue placeholder="Select">Camera:0</SelectValue>
            </SelectTrigger>
            <SelectContent position="popper">
              <SelectItem value="0">Camera:0</SelectItem>
            </SelectContent>
          </Select>
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
        <div className="flex w-[250px] flex-col gap-2">
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
          <Button className="h-20 w-full bg-blue-600 hover:bg-blue-500">
            Play
          </Button>
          <Button className="w-full">New Game</Button>
          <Button className="w-full">Move Suggestion</Button>
          <Button className="w-full">Analyze Match</Button>
          <Button className="w-full">Save History</Button>
          <h2 className="mt-4 text-xl font-semibold leading-none">
            Move History
          </h2>
          <Table className="max-h-[100px] w-full overflow-y-auto">
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Move</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow>
                <TableCell>1</TableCell>
                <TableCell>e5-e6</TableCell>
              </TableRow>
              <TableRow>
                <TableCell>2</TableCell>
                <TableCell>e5-e6</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </div>
      </section>
      <section className="container mt-4 grid items-center gap-2 py-2">
        <DebugImages />
      </section>
    </div>
  )
}
