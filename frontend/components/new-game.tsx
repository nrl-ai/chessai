"use client"

import { useState } from "react"
import { Button } from "@/registry/default/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/registry/default/ui/dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/registry/default/ui/select"
import { useToast } from "@/registry/default/ui/use-toast"

export function NewGame({ children }: { children: React.ReactNode }) {
  const { toast } = useToast()
  const [nextPlayer, setNextPlayer] = useState<string>("r")

  const newGame = () => {
    fetch("/api/xiangqi/new_game", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        next_player: nextPlayer,
      }),
    })
    toast({
      title: "New Game",
      description: "New game started.",
      duration: 3000,
    })
    setTimeout(() => {
      window.location.reload()
    }, 500)
  }

  return (
    <Dialog>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="sm:max-w-[475px]">
        <DialogHeader>
          <DialogTitle>New Game</DialogTitle>
          <DialogDescription>
            New game from the current board.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-2">
          <label htmlFor="next_player">Next Player</label>
          <Select
            onValueChange={(value) => setNextPlayer(value)}
            value={nextPlayer}
          >
            <SelectTrigger id="next_player">
              <SelectValue placeholder="Next Player">
                {"r" === nextPlayer ? "Red" : "Black"}
              </SelectValue>
            </SelectTrigger>
            <SelectContent position="popper">
              <SelectItem value={"r"} key={"r"}>
                Red
              </SelectItem>
              <SelectItem value={"b"} key={"b"}>
                Black
              </SelectItem>
            </SelectContent>
          </Select>
        </div>
        <DialogFooter>
          <Button
            className="w-full"
            onClick={() => {
              newGame()
            }}
          >
            Continue
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
