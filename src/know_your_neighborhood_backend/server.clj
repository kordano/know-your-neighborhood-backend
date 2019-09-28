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
            [know-your-neighborhood-backend.model]))

(defn ok [d] {:status 200 :body d})
(defn bad-request [d] {:status 400 :body d})
(defn body [req] (get-in req [:parameters :body]))
(defn path [req k] (get-in req [:parameters :path k]))

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
        {:get {:parameters {:query :know-your-neighborhood-backend.model/search}
               :handler (fn [req]
                          (ok {:foo :bar}))}}]]]
     {:data {:coercion reitit.coercion.spec/coercion
             :muuntaja m/instance
             :middleware [swagger/swagger-feature
                          parameters/parameters-middleware
                          muuntaja/format-negotiate-middleware
                          muuntaja/format-response-middleware
                          muuntaja/format-request-middleware
                          coercion/coerce-response-middleware
                          coercion/coerce-request-middleware
                          ]}})
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
