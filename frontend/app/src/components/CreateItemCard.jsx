import { Plus } from "lucide-react"
import { useState } from "react"
import axios from "axios"

import { Button } from "@/components/ui/button"
import {
	Item,
	ItemActions,
	ItemContent,
	ItemDescription,
	ItemTitle,
} from "@/components/ui/item"
import { Input } from "@/components/ui/input"

export function CreateItemCard({ refreshItems }) {
	const [title, setTitle] = useState("")
	const [description, setDescription] = useState("")

	const createItem = async () => {
		if (!title.trim()) return

		try {
			await axios.post("/api/v1/items/", { title, description })
			setTitle("")
			setDescription("")
			refreshItems()
		} catch (err) {
			console.error(err)
		}
	}

	return (
		<div className="flex w-full max-w-lg flex-col gap-6">
			<Item variant="outline">
				<ItemContent>
					<ItemTitle>
						<Input
							value={title}
							onChange={(e) => setTitle(e.target.value)}
							placeholder="Item title"
						/>
					</ItemTitle>
					<ItemDescription>
						<Input
							value={description}
							onChange={(e) => setDescription(e.target.value)}
							placeholder="Item description"
						/>
					</ItemDescription>
				</ItemContent>

				<ItemActions className="mt-auto">
					<Button
						size="icon-sm"
						variant="outline"
						className="rounded-full"
						onClick={createItem}
					>
						<Plus />
					</Button>
				</ItemActions>
			</Item>
		</div>
	)
}
