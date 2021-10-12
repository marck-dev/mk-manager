installDir=/etc/mk-d-manager
fileName=mk-manager
echo "Creating the intall directory..."
sudo mkdir -p $installDir
sleep 1
echo "Creating the executable"
touch $fileName
echo "#!/bin/bash" > $fileName
echo "cd $installDir &> /dev/null" >> $fileName
echo "python . \$@" >> $fileName
chmod +x $fileName
sleep 1
echo "Coping the files..."
sudo cp -r  . $installDir
echo "Creating the references..."
sudo ln -sf $installDir/$fileName /bin/$fileName
echo "Compiling sources..."
python -m compileall $installDir &> /dev/null
printf "\e[0;36mDone!\e[0m\n"
