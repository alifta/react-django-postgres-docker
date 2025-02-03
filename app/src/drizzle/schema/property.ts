import { relations } from "drizzle-orm";
import { pgTable, text } from "drizzle-orm/pg-core";
import { createdAt, id, updatedAt } from "../schemaHelpers";

export const PropertyTable = pgTable("property", {
	id,
	name: text().notNull(),
	description: text().notNull(),
	createdAt,
	updatedAt,
});

export const PropertyRelationships = relations(
	PropertyTable,
	({ one, many }) => ({
		test: one(),
	})
);
