/**
 * Une clases condicionales.
 *
 * La version de shadcn usa `clsx` + `tailwind-merge` para resolver clases de
 * Tailwind en conflicto. Aqui no hace falta: solo se concatenan clases sueltas
 * y `tailwind-merge` pesa mas que el propio componente del vortice.
 *
 * Si algun dia se adoptan componentes shadcn de verdad (que si dependen de esa
 * resolucion de conflictos), hay que cambiarla por:
 *     import { clsx, type ClassValue } from "clsx";
 *     import { twMerge } from "tailwind-merge";
 *     export const cn = (...i: ClassValue[]) => twMerge(clsx(i));
 */
export function cn(...classes: (string | false | null | undefined)[]): string {
  return classes.filter(Boolean).join(" ");
}
