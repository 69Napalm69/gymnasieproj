using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Pong : MonoBehaviour
{
    public GameObject leftPaddle;
    public GameObject rightPaddle;
    public TextMesh leftBoard;
    public TextMesh rightBoard;
    public CircleCollider2D ball;
    public float PaddleSpeed;
    public float BallSpeed;
    private int leftScore = 0;
    private int rightScore = 0;
    private int[] drives = new int[2] {1,1};

    // Update is called once per frame
    void Update()
    {
        //gets the directions the paddles are gonna move in
        float moveLeft = Input.GetAxis("Left");
        float moveRight = Input.GetAxis("Right");

        if (moveLeft != 0) // if left player is moving
        {
            // moves the paddle
            leftPaddle.transform.position = leftPaddle.transform.position + new Vector3(
                    0, // x
                    moveLeft * PaddleSpeed * Time.deltaTime, // y
                    0 // z
                );
        }
        
        if (moveRight != 0) // if right player is moving
        {
            // moves the paddle
            rightPaddle.transform.position = rightPaddle.transform.position + new Vector3(
                    0, // x
                    moveRight * PaddleSpeed * Time.deltaTime, // y
                    0 // z
                );
        }
        // moves the ball
        transform.position = transform.position + new Vector3(
                drives[0] * BallSpeed * Time.deltaTime, // x
                drives[1] * BallSpeed * Time.deltaTime, // y
                0 // z
            );
    }

    void OnTriggerEnter2D(Collider2D thing)
    {
        //the ball enters a 2D collider trigger, which can only be the scoring walls

        // point scoring
        if (this.transform.position.x > 0)
        {
            leftScore++;
            leftBoard.text = leftScore.ToString();
        } else
        {
            rightScore++;
            rightBoard.text = rightScore.ToString();
        }

        //reverses the direction in the x-axis 
        drives[0] *= -1;
        //resets ball
        this.transform.position = new Vector3(0, 0, 0);

    }

    void OnCollisionEnter2D(Collision2D collision)
    {
        //the ball collides with another 2D collider, it then checks the source and bounces accordingly

        // paddle bounces
        if(collision.gameObject == rightPaddle || collision.gameObject == leftPaddle)
        {
            // bounce off paddle
            drives[0] *= -1;
        } 
        //wall bounces
        else if (collision.gameObject.name == "BounceWalls")
        {
            //bounce off ceiling
            drives[1] *= -1;
        }
    }
}
