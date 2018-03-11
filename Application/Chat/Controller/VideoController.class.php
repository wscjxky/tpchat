<?php
namespace Chat\Controller;
use Think\Controller;
class VideoController extends Controller
{
    public function __construct()
    {
        parent::__construct();
       
    }
    public function index()
    {

        $this->display();


    }


}