import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const source = join(dirname(fileURLToPath(import.meta.url)), "entry.png");
const output = join(process.env.MAKEFUN_OUTPUT_DIR ?? "/output", "entry.png");

mkdirSync(dirname(output), { recursive: true });
copyFileSync(source, output);
