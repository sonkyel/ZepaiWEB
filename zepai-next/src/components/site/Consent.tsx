"use client";

/**
 * Consentimiento de cookies y carga de los rastreadores.
 *
 * Meta Pixel y Apollo estaban en la web antigua cargando desde la primera
 * linea del HTML, antes de que el visitante pudiera decir nada. Los dos
 * dejan cookies de terceros con fines publicitarios, asi que en Espana eso
 * incumple la LSSI y el RGPD: el consentimiento tiene que ser previo.
 *
 * Aqui no se carga nada hasta que alguien pulsa "Aceptar". Si rechaza o
 * ignora el aviso, no se descarga ni un byte de Meta ni de Apollo, y la web
 * funciona igual: los formularios van por EmailJS, que es necesario para
 * prestar el servicio que el propio visitante pide.
 *
 * La decision se guarda en localStorage, no en una cookie: para recordar una
 * negativa no hace falta poner justo lo que se acaba de rechazar.
 */

import { useEffect, useState } from "react";
import Link from "next/link";
import { T } from "@/lib/i18n";

const CLAVE = "zepai-consentimiento";
const PIXEL = "1520803392790499";
const APOLLO = "6a32a96ee978cc000c80f759";

type Decision = "todo" | "minimo" | null;

declare global {
  interface Window {
    fbq?: (...args: unknown[]) => void;
    _fbq?: unknown;
    trackingFunctions?: { onLoad: (o: { appId: string }) => void };
  }
}

let yaCargado = false;

/** Descarga Meta Pixel y Apollo. Solo se llama con consentimiento dado. */
function cargarRastreadores() {
  if (yaCargado || typeof window === "undefined") return;
  yaCargado = true;

  // Meta Pixel, con el mismo identificador que la web anterior
  if (!window.fbq) {
    const n: any = function (...args: unknown[]) {
      n.callMethod ? n.callMethod.apply(n, args) : n.queue.push(args);
    };
    n.push = n;
    n.loaded = true;
    n.version = "2.0";
    n.queue = [];
    window.fbq = n;
    window._fbq = n;
    const s = document.createElement("script");
    s.async = true;
    s.src = "https://connect.facebook.net/en_US/fbevents.js";
    document.head.appendChild(s);
  }
  window.fbq?.("init", PIXEL);
  window.fbq?.("track", "PageView");

  // Apollo, con cache invalidada como en el original
  const a = document.createElement("script");
  a.src =
    "https://assets.apollo.io/micro/website-tracker/tracker.iife.js?nocache=" +
    Math.random().toString(36).substring(7);
  a.async = true;
  a.defer = true;
  a.onload = () => window.trackingFunctions?.onLoad({ appId: APOLLO });
  document.head.appendChild(a);
}

export function Consent() {
  const [decision, setDecision] = useState<Decision>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const guardado = localStorage.getItem(CLAVE) as Decision;
    if (guardado === "todo") {
      setDecision("todo");
      cargarRastreadores();
    } else if (guardado === "minimo") {
      setDecision("minimo");
    } else {
      // Un respiro antes de aparecer: el aviso no debe competir con el hero
      const t = setTimeout(() => setVisible(true), 900);
      return () => clearTimeout(t);
    }
  }, []);

  const decidir = (valor: Exclude<Decision, null>) => {
    localStorage.setItem(CLAVE, valor);
    setDecision(valor);
    setVisible(false);
    if (valor === "todo") cargarRastreadores();
  };

  if (decision || !visible) return null;

  return (
    <div className="cookies" role="dialog" aria-live="polite" aria-label="Cookies">
      <p className="cookies-txt">
        <T
          es="Usamos cookies de Meta y Apollo para medir de dónde llegan las visitas. No se activan hasta que lo aceptas."
          en="We use Meta and Apollo cookies to measure where visits come from. They do not run until you accept."
        />{" "}
        <Link href="/politica-de-cookies">
          <T es="Más detalles" en="More details" />
        </Link>
      </p>
      <div className="cookies-btns">
        <button type="button" className="cookies-no" onClick={() => decidir("minimo")}>
          <T es="Solo lo necesario" en="Only what is needed" />
        </button>
        <button type="button" className="cookies-si" onClick={() => decidir("todo")}>
          <T es="Aceptar" en="Accept" />
        </button>
      </div>
    </div>
  );
}
