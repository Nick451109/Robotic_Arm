using UnityEngine;
using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

public class HandTracking : MonoBehaviour
{
    public UDPReceive udpReceive; // Componente que recibe datos UDP
    public Transform wristJoint; // Parte del brazo que rota con la muñeca
    public Transform thumbJoint; // Parte del brazo que rota con el pulgar
    public Transform indexJoint; // Parte del brazo que rota con el índice

    // Aquí definirías los ejes de rotación para cada parte del brazo
    private Vector3 wristAxis = Vector3.up; // Por ejemplo, rotar alrededor del eje Y
    private Vector3 thumbAxis = Vector3.forward; // Por ejemplo, rotar alrededor del eje Z
    private Vector3 indexAxis = Vector3.forward; // Por ejemplo, rotar alrededor del eje Z

    void Update()
    {
        if (!string.IsNullOrEmpty(udpReceive.data))
        {
            ProcessData(udpReceive.data);
        }
    }

    void ProcessData(string data)
        {
            // Divide el string recibido en partes
            string[] splitData = data.Split(',');

            // Asegúrate de que los datos recibidos son los esperados
            if (splitData.Length == 4)
            {
                // Extrae el valor de rotación y convierte a float
                float rotationValue = float.Parse(splitData[1]); // Asume que este es el valor adecuado para la rotación

                // Aplica la rotación basada en la parte del cuerpo
                switch (splitData[0])
                {
                    case "wrist":
                        ApplyRotation(wristJoint, Vector3.up, rotationValue);
                        break;
                    case "thumb":
                        ApplyRotation(thumbJoint, thumbAxis, rotationValue);
                        break;
                    case "index":
                        ApplyRotation(indexJoint, indexAxis, rotationValue);
                        break;
                }
            }
        }

    void ApplyRotation(Transform joint, Vector3 axis, float rotationValue)
        {
            // Define el ángulo máximo de subida y bajada de la muñeca
            float maxUpRotation = 120.0f; // Aumenta este valor para un movimiento más pronunciado
            float maxDownRotation = -120.0f; // Aumenta este valor para un movimiento más pronunciado

            // Limita el valor de rotación dentro del rango de subida y bajada
            rotationValue = Mathf.Clamp(rotationValue, maxDownRotation, maxUpRotation);

            // Calcula la rotación basada en el valor limitado
            Quaternion newRotation = Quaternion.Euler(0, rotationValue, 0); // Girar en el eje Y

            // Aplica la rotación a la muñeca
            joint.localRotation = Quaternion.Lerp(joint.localRotation, newRotation, Time.deltaTime * 5);
        }
}