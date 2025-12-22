import { Minus } from "lucide-react"
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

export function ItemCard({ id, title, description, refreshItems }) {
	const [localTitle, setLocalTitle] = useState(title)
	const [localDescription, setLocalDescription] = useState(description)
	console.log(id);
	const updateItem = async () => {
		try {
			await axios.patch(`/api/v1/items/${id}`, {
				title: localTitle,
				description: localDescription,
			})
			refreshItems()
		} catch (err) {
			console.error(err)
		}
	}

	const deleteItem = async () => {
		try {
			await axios.delete(`/api/v1/items/${id}`)
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
							value={localTitle}
							onChange={(e) => setLocalTitle(e.target.value)}
							onBlur={updateItem}
						/>
					</ItemTitle>
					<ItemDescription>
						<Input
							value={localDescription}
							onChange={(e) => setLocalDescription(e.target.value)}
							onBlur={updateItem}
						/>
					</ItemDescription>
				</ItemContent>

				<ItemActions className="mt-auto">
					<Button
						size="icon-sm"
						variant="outline"
						className="rounded-full"
						onClick={deleteItem}
					>
						<Minus />
					</Button>
				</ItemActions>
			</Item>
		</div>
	)
}
