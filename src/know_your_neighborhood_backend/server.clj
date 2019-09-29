(ns know-your-neighborhood-backend.server
  (:require [reitit.http :as http]
            [reitit.ring :as ring]
            [muuntaja.core :as m]
            [reitit.swagger :as swagger]
            [reitit.swagger-ui :as swagger-ui]
            [clj-time.core :as time]
            [reitit.coercion.spec]
            [reitit.ring.coercion :as coercion]
            [reitit.ring.middleware.parameters :as parameters]
            [reitit.ring.middleware.muuntaja :as muuntaja]
            [reitit.interceptor.sieppari :as sieppari]
            [reitit.ring.coercion :as rrc]
            [ring.middleware.cors :refer [wrap-cors]]
            [clojure.spec.alpha :as s]
            [mount.core :refer [defstate]]
            [org.httpkit.server :as kit]
            [clojure.java.shell :as shell]
            [clojure.string :as string]
            [clojure.data.json :as json]
            [clojure.java.shell :as sh]))

(defn ok [d] {:status 200 :body d})
(defn bad-request [d] {:status 400 :body d})
(defn body [req] (get-in req [:parameters :body]))
(defn path [req k] (get-in req [:parameters :path k]))

(s/def :search/checkAddressLat double?)
(s/def :search/checkAddressLon double?)
(s/def :search/targetAddressLat double?)
(s/def :search/targetAddressLon double?)

(s/def ::search (s/keys :req-un [:search/checkAddressLat :search/checkAddressLon :search/targetAddressLat :search/targetAddressLon]))

(defn parse-distance [raw-py-results]
  (->> (string/split raw-py-results #"\n")
       (map #(->> (string/split % #",")
                  (zipmap [:additionalText :distance :lat :lon :service])))))

;; "" // 'red' | 'darkred' | 'orange' | 'green' | 'darkgreen' | 'blue' | 'purple' | 'darkpurple' | 'cadetblue',
(def service-color
  {"health" "green"
   "safety" "red"
   "daycare" "purple"
   "education" "blue"
   "traffic" "darkred"
   "culture" "darkgreen"})

(def app
  (->
   (ring/ring-handler
    (ring/router
     [["/swagger.json"
       {:get {:no-doc true
              :swagger {:info {:title "Know your neighborhood API"
                               :description ""}}
              :handler (swagger/create-swagger-handler)}}]
      ["/api"
       ["/search"
        {:get {:parameters {:query ::search}
               :handler (fn [{{coords :query} :parameters}]
                          (let [distance-out (:out (sh/sh "python" "lamia_main.py" (str (:checkAddressLon coords)) (str (:checkAddressLat coords)) ))
                                distances (parse-distance distance-out )
                                next-station (select-keys (clojure.set/rename-keys (first distances) {:additionalText :name}) [:name :distance])
                                distances (rest distances)
                                next-termimal (select-keys (clojure.set/rename-keys (first distances) {:additionalText :name}) [:name :distance])
                                distances (rest distances)
                                freqs (frequencies (map :service distances))
                                drawing (->> distances
                                             (map (fn [r] (-> r
                                                              (assoc :type "Marker"
                                                                     :tooltip (:additionalText r)
                                                                     :popup (:service r)
                                                                     :markerColor (get service-color (:service r)))
                                                              (dissoc :distance :service))))
                                             (into #{})
                                             vec)
                                a-to-b (json/read-str (:out (sh/sh "python3" "pythonscripts/a_to_b.py" (str (:checkAddressLat coords)) (str (:checkAddressLon coords)) (str (:targetAddressLat coords)) (str (:targetAddressLon coords)))))
                                a-to-b-drawing (map
                                                (fn [c]
                                                  {:type "Polyline"
                                                   :coordinates (mapv (fn [coords] (first (vec (vals coords)))) (get c "Geometry"))
                                                   :color "orange"
                                                   :popup (str "CO2: " (get c "co2_emissions") ", time: " (get c "Duration_mins") ", steps: " (get c "Itinerary_Desc"))
                                                   :tooltip (get c "Duration_mins")})
                                                a-to-b)]
                            (ok {:results [{:nextBike next-station}
                                           {:nextTerminal next-termimal}
                                           {:services freqs}
                                           {:itineraries (into {}
                                                               (mapv
                                                                (fn [c] [(get c "Itinerary_Desc")
                                                                         (str (get c "Duration_mins") " mins, " (get c "co2_emissions") " CO2")])
                                                                a-to-b))}]
                                 :drawable (concat drawing a-to-b-drawing)})))}}]]]
     {:data {:coercion reitit.coercion.spec/coercion
             :muuntaja m/instance
             :middleware [swagger/swagger-feature
                          parameters/parameters-middleware
                          muuntaja/format-negotiate-middleware
                          muuntaja/format-response-middleware
                          muuntaja/format-request-middleware
                          coercion/coerce-response-middleware
                          coercion/coerce-request-middleware]}})
    (ring/routes
     (swagger-ui/create-swagger-ui-handler
      {:path "/"
       :config {:validatorUrl nil :operationsSorter "alpha"}})
     (ring/create-default-handler))
    {:executor sieppari/executor})
   (wrap-cors :access-control-allow-origin [#"http://localhost" #"http://localhost:9000/*" #"http://localhost:3000"]
              :access-control-allow-methods [:get :put :post :delete])))

(defstate server
  :start (kit/run-server app {:port 3000})
  :stop (server))
